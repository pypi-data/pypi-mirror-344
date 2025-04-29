# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 17:17
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : base_extra.py
import copy
import csv
import json
import types

from ultipa.structs.InsertErrorCode import  InsertErrorCodeMap
from ultipa.types.types import CodeMap
from ultipa.types.types_response import *
from ultipa import ParameterException
from ultipa.configuration import InsertRequestConfig
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.connection.clientType import ClientType
from ultipa.connection.commonUql import GetPropertyBySchema
from ultipa.connection.connectionBase import ConnectionBase
from ultipa.connection.uqlHelper import UQLHelper
from ultipa.proto import ultipa_pb2
from ultipa.structs import DBType, Node, Edge
from ultipa.structs.Retry import Retry
from ultipa.structs.Schema import Schema
from ultipa.types import ULTIPA, ULTIPA_REQUEST
from ultipa.types.types_response import PropertyTable, QueryResponseListener
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertTableToDict, convertToListAnyObject, convertToStats
from ultipa.utils.format import FormatType
from ultipa.utils.noneCheck import checkNone
from ultipa.utils.raftRetry import RetryHelp
from ultipa.utils.ultipa_datetime import getTimeZoneOffset, getTimeOffsetSeconds
from ultipa.structs.QLType import QLType

class BaseExtra(ConnectionBase):
	'''
		Processing class that defines settings for basic operations.

	'''

	def test(self,
			 config: RequestConfig = RequestConfig()) -> bool:
		'''
		Test connection.

		Args:
			config: An object of RequestConfig class

		Returns:
			Response
		'''
		returnReq = ULTIPA.ReturnReq(config.graph, "test", None, None, False)
		try:
			clientInfo = self.getClientInfo(useHost=config.host)
			name = 'Test'
			res = clientInfo.Controlsclient.SayHello(ultipa_pb2.HelloUltipaRequest(name=name),
													 metadata=clientInfo.metadata)
			returnReq.host = clientInfo.host
			if (res.status.error_code == ErrorCode.SUCCESS.value):
				return True
		except Exception as e:
			raise e
		return False


	def exportData(self, request: ULTIPA_REQUEST.ExportRequest, cb: Callable[[List[Node], List[Edge]],None],
				   config: RequestConfig = RequestConfig()):
		try:
			req = ultipa_pb2.ExportRequest(db_type=request.dbType.value, limit=-1,
										   select_properties=request.selectProperties, schema=request.schema)

			graphName = request.graph if not checkNone(request.graph) else config.graph
			clientInfo = self.getClientInfo(graphSetName=graphName)
			res = clientInfo.Controlsclient.Export(req, metadata=clientInfo.metadata)
			nodedata = []
			edgedata = []
			response = UltipaResponse()
			for exportReply in res:
				response.status = FormatType.status(exportReply.status)
				if exportReply.node_table:
					nodedata = FormatType.export_nodes(exportReply, config.timeZone, config.timeZoneOffset)
				if exportReply.edge_table:
					edgedata = FormatType.export_edges(exportReply, config.timeZone, config.timeZoneOffset)
				if nodedata:
					uql = ULTIPA.ExportReply(data=nodedata)
					response.data = uql.data
					cb(uql.data,None)
				if edgedata:
					uql = ULTIPA.ExportReply(data=edgedata)
					response.data = uql.data
					cb(None,uql.data)

		except Exception as e:
			errorRes = UltipaResponse()
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
				print(message)
			except:
				message = 'UNKNOW ERROR'
				print(message)
			errorRes.status = ULTIPA.Status(code=ULTIPA.ErrorCode.UNKNOW_ERROR, message=message)
			return errorRes

	def uql(self, uql: str,
			config: RequestConfig = RequestConfig()) -> Response:
		'''
		Execute UQL.

		Args:
			uql: A uql statement

			config: An object of RequestConfig class

		Returns:
			Response

		'''
		request = ultipa_pb2.QueryRequest()
		request.query_text = uql
		request.query_type = QLType.UQL
		if self.getTimeout(config.timeout):
			request.timeout = self.getTimeout(config.timeout)
		if config.thread is not None:
			request.thread_num = config.thread
		ultipaRes = Response()
		if config.graph == '' and self.defaultConfig.defaultGraph != '':
			config.graph = self.defaultConfig.defaultGraph

		if self.defaultConfig.maxRecvSize != self.hostManagerControl.maxRecvSize:
			self.hostManagerControl.maxRecvSize = self.defaultConfig.maxRecvSize
		onRetry = copy.deepcopy(Retry())
		canRetry=True
		while onRetry.current < onRetry.max and canRetry:
			try:
				import pytz
				getTimeZoneOffset(config, self.defaultConfig)
				timeZone = config.timeZone
				timeZoneOffset = config.timeZoneOffset
				timeZoneOffset = getTimeOffsetSeconds(timeZoneOffset)
				clientInfo = self.getClientInfo(graphSetName=config.graph, uql=uql,
												useHost=config.host,
												timezone=timeZone,
												timeZoneOffset=timeZoneOffset)
				uqlIsExtra = UQLHelper.uqlIsExtra(uql)
				if uqlIsExtra:
					res = clientInfo.Controlsclient.QueryEx(request, metadata=clientInfo.metadata)
				else:
					res = clientInfo.Rpcsclient.Query(request, metadata=clientInfo.metadata)

				ultipaRes = FormatType.uqlMergeResponse(res, timeZone, timeZoneOffset)


				if not isinstance(ultipaRes, types.GeneratorType) and RetryHelp.checkRes(ultipaRes):
					onRetry.current += 1
					continue
				else:
					return ultipaRes

			except Exception as e:
				try:
					message = str(e._state.code) + ' : ' + str(e._state.details)
				except:
					message = str(e)
				ultipaRes.status = ULTIPA.Status(code=ULTIPA.ErrorCode.UNKNOW_ERROR, message=message)
				if ultipaRes.status.code not in {ULTIPA.ErrorCode.RAFT_REDIRECT, ULTIPA.ErrorCode.RAFT_LEADER_NOT_YET_ELECTED, ULTIPA.ErrorCode.RAFT_NO_AVAILABLE_FOLLOWERS,ULTIPA.ErrorCode.RAFT_NO_AVAILABLE_ALGO_SERVERS}:
					canRetry=False
				else:
					onRetry.current += 1
					self.hostManagerControl.getHostManger(config.graph).raftReady = False


		return ultipaRes

	def uqlStream(self, uql: str, cb: QueryResponseListener, config: RequestConfig = RequestConfig()):

		'''
		Execute UQL.

		Args:
			uql: A uql statement

			cb: Listener for the streaming process.

			config: An object of RequestConfig class

		'''
		cb.emit("start", config)
		request = ultipa_pb2.QueryRequest()
		request.query_text = uql
		request.query_type = QLType.UQL
		if self.getTimeout(config.timeout):
			request.timeout = self.getTimeout(config.timeout)
		if config.thread is not None:
			request.thread_num = config.thread


		if self.defaultConfig.maxRecvSize != self.hostManagerControl.maxRecvSize:
			self.hostManagerControl.maxRecvSize = self.defaultConfig.maxRecvSize
		onRetry = copy.deepcopy(Retry())
		while onRetry.current < onRetry.max:
			try:
				import pytz
				getTimeZoneOffset(config, self.defaultConfig)
				timeZone = config.timeZone
				timeZoneOffset = config.timeZoneOffset
				timeZoneOffset = getTimeOffsetSeconds(timeZoneOffset)
				clientInfo = self.getClientInfo(graphSetName=config.graph, uql=uql,
												useHost=config.host,
												 timezone=timeZone,
												timeZoneOffset=timeZoneOffset)
				uqlIsExtra = UQLHelper.uqlIsExtra(uql)
				if uqlIsExtra:
					res = clientInfo.Controlsclient.QueryEx(request, metadata=clientInfo.metadata)
				else:
					res = clientInfo.Rpcsclient.Query(request, metadata=clientInfo.metadata)

				uql_response = UltipaResponse()
				ultipa_response = Response()
				for uqlReply in res:
					status = FormatType.status(uqlReply.status)
					uql_response = FormatType.response(uql_response, uqlReply, timeZone, timeZoneOffset)
					ret = ULTIPA.UqlReply(dataBase=uql_response.data)

					if status.code != ULTIPA.ErrorCode.SUCCESS:
						ultipa_response.status = uql_response.status
						cb.emit("end", config)
						return

					ultipa_response.items = ret._aliasMap
					ultipa_response.status = uql_response.status
					ultipa_response.statistics = uql_response.statistics
					should_continue = cb.emit("data", ultipa_response, config)
					if should_continue == False:
						cb.emit("end", config)
						return

				if not isinstance(ultipa_response, types.GeneratorType) and RetryHelp.checkRes(ultipa_response):
					onRetry.current += 1
					continue
				else:
					cb.emit("end", config)
					return

			except Exception as e:
				ultipaRes = Response()
				onRetry.current += 1
				self.hostManagerControl.getHostManger(config.graph).raftReady = False
				try:
					message = str(e._state.code) + ' : ' + str(e._state.details)
				except:
					message = str(e)
				ultipaRes.status = ULTIPA.Status(code=ULTIPA.ErrorCode.UNKNOW_ERROR, message=message)
				print(ultipaRes.status.message)
		cb.emit("end", config)
		return

	def gql(self, gql: str,
			config: RequestConfig = RequestConfig()) -> Response:
		'''
		Execute GQL.

		Args:
			gql: A gql statement

			config: An object of RequestConfig class

		Returns:
			Response

		'''
		request = ultipa_pb2.QueryRequest()
		request.query_text = gql
		request.query_type = QLType.GQL
		if self.getTimeout(config.timeout):
			request.timeout = self.getTimeout(config.timeout)
		if config.thread is not None:
			request.thread_num = config.thread
		ultipaRes = Response()
		if config.graph == '' and self.defaultConfig.defaultGraph != '':
			config.graph = self.defaultConfig.defaultGraph


		if self.defaultConfig.maxRecvSize != self.hostManagerControl.maxRecvSize:
			self.hostManagerControl.maxRecvSize = self.defaultConfig.maxRecvSize
		onRetry = copy.deepcopy(Retry())
		canRetry = True
		while onRetry.current < onRetry.max and canRetry:
			try:
				import pytz
				getTimeZoneOffset(config, self.defaultConfig)
				timeZone = config.timeZone
				timeZoneOffset = config.timeZoneOffset
				timeZoneOffset = getTimeOffsetSeconds(timeZoneOffset)
				clientInfo = self.getClientInfo(graphSetName=config.graph, uql=gql,
												useHost=config.host,
												timezone=timeZone,
												timeZoneOffset=timeZoneOffset)
				uqlIsExtra = UQLHelper.uqlIsExtra(gql)
				if uqlIsExtra:
					res = clientInfo.Controlsclient.QueryEx(request, metadata=clientInfo.metadata)
				else:
					res = clientInfo.Rpcsclient.Query(request, metadata=clientInfo.metadata)


				ultipaRes = FormatType.uqlMergeResponse(res, timeZone, timeZoneOffset)

				if not isinstance(ultipaRes, types.GeneratorType) and RetryHelp.checkRes(ultipaRes):
					onRetry.current += 1
					continue
				else:
					return ultipaRes

			except Exception as e:
				try:
					message = str(e._state.code) + ' : ' + str(e._state.details)
				except:
					message = str(e)
				ultipaRes.status = ULTIPA.Status(code=ULTIPA.ErrorCode.UNKNOW_ERROR, message=message)

				if ultipaRes.status.code not in {ULTIPA.ErrorCode.RAFT_REDIRECT, ULTIPA.ErrorCode.RAFT_LEADER_NOT_YET_ELECTED,
												 ULTIPA.ErrorCode.RAFT_NO_AVAILABLE_FOLLOWERS,
												 ULTIPA.ErrorCode.RAFT_NO_AVAILABLE_ALGO_SERVERS}:
					canRetry = False
				else:
					onRetry.current += 1
					self.hostManagerControl.getHostManger(config.graph).raftReady = False

		return ultipaRes

	def gqlStream(self, gql: str, cb: QueryResponseListener, config: RequestConfig = RequestConfig()):

		'''
		Execute UQL.

		Args:
			gql: A gql statement

			cb: Listener for the streaming process.

			config: An object of RequestConfig class

		'''
		cb.emit("start", config)
		request = ultipa_pb2.QueryRequest()
		request.query_text = gql
		request.query_type = QLType.GQL
		if self.getTimeout(config.timeout):
			request.timeout = self.getTimeout(config.timeout)
		if config.thread is not None:
			request.thread_num = config.thread
		if config.graph == '' and self.defaultConfig.defaultGraph != '':
			config.graph = self.defaultConfig.defaultGraph


		if self.defaultConfig.maxRecvSize != self.hostManagerControl.maxRecvSize:
			self.hostManagerControl.maxRecvSize = self.defaultConfig.maxRecvSize
		onRetry = copy.deepcopy(Retry())
		while onRetry.current < onRetry.max:
			try:
				import pytz
				getTimeZoneOffset(config, self.defaultConfig)
				timeZone = config.timeZone
				timeZoneOffset = config.timeZoneOffset
				timeZoneOffset = getTimeOffsetSeconds(timeZoneOffset)
				clientInfo = self.getClientInfo(graphSetName=config.graph, uql=gql,
												useHost=config.host,
												timezone=timeZone,
												timeZoneOffset=timeZoneOffset)
				uqlIsExtra = UQLHelper.uqlIsExtra(gql)
				if uqlIsExtra:
					res = clientInfo.Controlsclient.QueryEx(request, metadata=clientInfo.metadata)
				else:
					res = clientInfo.Rpcsclient.Query(request, metadata=clientInfo.metadata)

				uql_response = UltipaResponse()
				ultipa_response = Response()
				for uqlReply in res:
					status = FormatType.status(uqlReply.status)
					uql_response = FormatType.response(uql_response, uqlReply, timeZone, timeZoneOffset)
					ret = ULTIPA.UqlReply(dataBase=uql_response.data)

					if status.code != ULTIPA.ErrorCode.SUCCESS:
						ultipa_response.status = uql_response.status
						cb.emit("end", config)
						return

					ultipa_response.items = ret._aliasMap
					ultipa_response.status = uql_response.status
					ultipa_response.statistics = uql_response.statistics
					should_continue = cb.emit("data", ultipa_response, config)
					if should_continue == False:
						cb.emit("end", config)
						return

				if not isinstance(ultipa_response, types.GeneratorType) and RetryHelp.checkRes(ultipa_response):
					onRetry.current += 1
					continue
				else:
					cb.emit("end", config)
					return

			except Exception as e:
				ultipaRes = Response()
				onRetry.current += 1
				self.hostManagerControl.getHostManger(config.graph).raftReady = False
				try:
					message = str(e._state.code) + ' : ' + str(e._state.details)
				except:
					message = str(e)
				ultipaRes.status = ULTIPA.Status(code=ULTIPA.ErrorCode.UNKNOW_ERROR, message=message)
				print(ultipaRes.status.message)
		cb.emit("end", config)
		return



	def uqlSingle(self, uqlMaker: UQLMAKER) -> Response:
		res = self.uql(uqlMaker.toString(), uqlMaker.commonParams)
		return res

	def UqlListSimple(self, uqlMaker: UQLMAKER, responseKeyFormat: ResponseKeyFormat = None,
					  isSingleOne: bool = True) -> Response:
		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.ErrorCode.SUCCESS:
			simplrRes = UltipaResponse(res.status, res.items)
			return simplrRes

		if not isSingleOne:
			retList = []
			for alias in res.aliases:
				item = res.items.get(alias.name)
				table = item.entities
				table_rows = table.rows
				table_rows_dict = convertTableToDict(table_rows, table.headers)
				if responseKeyFormat:
					table_rows_dict = responseKeyFormat.changeKeyValue(table_rows_dict)
				data = convertToListAnyObject(table_rows_dict)
				retList.append(PropertyTable(name=table.name, data=data))
			simplrRes = UltipaResponse(res.status, retList)
			return simplrRes

		alisFirst = res.aliases[0].name if len(res.aliases) > 0 else None
		firstItem = res.items.get(alisFirst)
		if firstItem:
			table_rows = firstItem.entities.rows
			table_rows_dict = convertTableToDict(table_rows, firstItem.entities.headers)
			if responseKeyFormat:
				table_rows_dict = responseKeyFormat.changeKeyValue(table_rows_dict)
			data = convertToListAnyObject(table_rows_dict)
			simplrRes = UltipaResponse(res.status, data)
			simplrRes.statistics = res.statistics
			return simplrRes
		else:
			return res

	def UqlUpdateSimple(self, uqlMaker: UQLMAKER):
		res = self.uqlSingle(uqlMaker)
		return UltipaResponse(res.status, statistics=res.statistics)

	def insertNodesBatchBySchema(self, schema: Schema, nodes: List[Node],
								 config: InsertRequestConfig) -> InsertResponse:
		'''
		Batch insert nodes of a same schema (that already exists in the graph).

		Args:
			schema:  The target schema; the attributes name and dbType are mandatory, properties should include some or all properties.

			nodes: The data to be inserted, List[Node]

			config: An object of InsertConfig class

		Returns:
			InsertResponse

		'''

		if checkNone(schema.name) or not isinstance(schema.properties,list) :
			messege = 'The name of schema cannot be None' if checkNone(schema.name) else 'The properties type of schema must be list'
			return Response(status=Status(code=ErrorCode.PARAM_ERROR,message=messege))

		if config.graph == '' and self.defaultConfig.defaultGraph != '':
			config.graph = self.defaultConfig.defaultGraph

		clientInfo = self.getClientInfo(clientType=ClientType.Update, graphSetName=config.graph
										)

		nodetable = FormatType.makeEntityNodeTable(schema, nodes, getTimeZoneOffset(requestConfig=config,
																				   defaultConfig=self.defaultConfig))

		_nodeTable = ultipa_pb2.EntityTable(schemas=nodetable.schemas, entity_rows=nodetable.nodeRows)
		request = ultipa_pb2.InsertNodesRequest()
		request.silent = config.silent
		request.insert_type = config.insertType.value
		request.graph_name = config.graph
		request.node_table.MergeFrom(_nodeTable)
		res = clientInfo.Rpcsclient.InsertNodes(request, metadata=clientInfo.metadata)

		status = FormatType.status(res.status)
		uqlres = InsertResponse(status=status)
		reTry = RetryHelp.check(self, config, uqlres)
		if reTry.canRetry:
			return self.insertNodesBatchBySchema(schema, nodes, config)

		uqlres.uuids = [i for i in res.uuids]
		uqlres.ids = [i for i in res.ids]
		errorDict = {}
		for i, data in enumerate(res.ignore_error_code):
			try:
				index = nodes[res.ignore_indexes[i]]._getIndex()
			except Exception as e:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			if index is None:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			errorDict.update({index: InsertErrorCodeMap.getUnsertErrorCode(data)})
		uqlres.errorItems = {key :errorDict[key] for key in sorted(errorDict.keys())}
		return uqlres

	def insertEdgesBatchBySchema(self, schema: Schema, edges: List[Edge],
								 config: InsertRequestConfig) -> InsertResponse:
		'''
		Batch insert edges of a same schema (that already exists in the graph)

		Args:
			schema: The target schema; the attributes name and dbType are mandatory, properties should include some or all properties.

			edges: The list of edges to be inserted; the attributes fromId and toId of each Edge are mandatory, uuid, fromUuid, and toUuid cannot be set, values must have the same structure with Schema.properties.

			config: An object of InsertConfig class

		Returns:
			InsertResponse

		'''
		if checkNone(schema.name) or not isinstance(schema.properties,list) :
			messege = 'The name of schema cannot be None' if checkNone(schema.name) else 'The properties type of schema must be list'
			return Response(status=Status(code=ErrorCode.PARAM_ERROR, message=messege))
		if config.graph == '' and self.defaultConfig.defaultGraph != '':
			config.graph = self.defaultConfig.defaultGraph

		clientInfo = self.getClientInfo(clientType=ClientType.Update, graphSetName=config.graph
										)

		edgetable = FormatType.makeEntityEdgeTable(schema=schema, rows = edges,
												   timeZoneOffset=getTimeZoneOffset(requestConfig=config,
																					defaultConfig=self.defaultConfig))

		_edgeTable = ultipa_pb2.EntityTable(schemas=edgetable.schemas, entity_rows=edgetable.edgeRows)
		request = ultipa_pb2.InsertEdgesRequest()
		request.silent = config.silent
		request.insert_type = config.insertType.value
		request.graph_name = config.graph
		request.edge_table.MergeFrom(_edgeTable)
		res = clientInfo.Rpcsclient.InsertEdges(request, metadata=clientInfo.metadata)

		status = FormatType.status(res.status)
		uqlres = InsertResponse(status=status)
		reTry = RetryHelp.check(self, config, uqlres)
		if reTry.canRetry:
			return self.insertEdgesBatchBySchema(schema, edges, config)

		uqlres.uuids = [i for i in res.uuids]
		errorDict = {}
		for i, data in enumerate(res.ignore_error_code):
			try:
				index = edges[res.ignore_indexes[i]]._getIndex()
			except Exception as e:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			if index is None:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			errorDict.update({index: InsertErrorCodeMap.getUnsertErrorCode(data)})
		uqlres.errorItems = {key :errorDict[key] for key in sorted(errorDict.keys())}
		return uqlres

	def insertNodesBatchAuto(self, nodes: List[Node],
							 config: InsertRequestConfig) -> Dict[str,InsertResponse]:
		'''
		Batch insert nodes of different schemas (that will be created if not existent)

		Args:
			nodes: The data to be inserted, List[Node]

			config: An object of InsertConfig class

		Returns:
			Dict[str,InsertResponse]

		'''
		Result = {}
		schemaDict = {}
		batches = {}
		schemaRet = self.uql(GetPropertyBySchema.node, config)
		if schemaRet.status.code == ULTIPA.ErrorCode.SUCCESS:
			for aliase in schemaRet.aliases:
				if aliase.name == '_nodeSchema':
					schemaDict = convertTableToDict(schemaRet.alias(aliase.name).entities.rows,
													schemaRet.alias(aliase.name).entities.headers)
			if not schemaDict:
				raise ParameterException(err='Please create Node Schema.')
		else:
			raise ParameterException(err=schemaRet.status.message)
		for index, node in enumerate(nodes):
			node._index = index
			if batches.get(node.schema) is None:
				batches[node.schema] = ULTIPA_REQUEST.Batch()
				find = list(filter(lambda x: x.get('name') == node.schema, schemaDict))
				if find:
					findSchema = find[0]
					propertyList = FormatType.checkProperty(node, json.loads(findSchema.get("properties")))
					reqSchema = ULTIPA_REQUEST.Schema(name=node.schema, properties=propertyList,dbType=DBType.DBNODE)
					batches[node.schema].Schema = reqSchema
				else:
					if node.schema is None:
						raise ParameterException(err=f"Row [{index}]:Please set schema name for node.")
					else:
						raise ParameterException(err=f"Row [{index}]:Node Schema not found {node.schema}.")

			batches.get(node.schema).Nodes.append(node)
		for key in batches:
			batch = batches.get(key)
			ret = self.insertNodesBatchBySchema(schema=batch.Schema, nodes=batch.Nodes, config=config)
			Result.update(
				{key:ret })
		return Result


	def insertEdgesBatchAuto(self, edges: List[Edge],
							 config: InsertRequestConfig) -> Dict[str,InsertResponse]:
		'''
		Batch insert edges of different schemas (that will be created if not existent)

		Args:
			edges: The data to be inserted, List[Edge]

			config: An object of InsertConfig class

		Returns:
			Dict[str,InsertResponse]

		'''
		Result = {}
		schemaDict = []
		batches = {}
		schemaRet = self.uql(GetPropertyBySchema.edge, config)
		if schemaRet.status.code == ULTIPA.ErrorCode.SUCCESS:
			for aliase in schemaRet.aliases:
				if aliase.name == '_edgeSchema':
					schemaDict = convertTableToDict(schemaRet.alias(aliase.name).entities.rows,
													schemaRet.alias(aliase.name).entities.headers)
			if not schemaDict:
				raise ParameterException(err='Please create Edge Schema.')
		else:
			raise ParameterException(err=schemaRet.status.message)
		for index, edge in enumerate(edges):
			edge._index = index
			if batches.get(edge.schema) == None:
				batches[edge.schema] = ULTIPA_REQUEST.Batch()
				find = list(filter(lambda x: x.get('name') == edge.schema, schemaDict))
				if find:
					findSchema = find[0]
					propertyList = FormatType.checkProperty(edge, json.loads(findSchema.get("properties")))
					reqSchema = ULTIPA_REQUEST.Schema(name=edge.schema, properties=propertyList,dbType=DBType.DBEDGE)
					batches[edge.schema].Schema = reqSchema
				else:
					if edge.schema is None:
						raise ParameterException(err=f"Row [{index}]:Please set schema name for edge.")
					else:
						raise ParameterException(err=f"Row [{index}]:Edge Schema not found {edge.schema}.")
			batches.get(edge.schema).Edges.append(edge)
		for key in batches:
			batch = batches.get(key)
			ret = self.insertEdgesBatchBySchema(schema=batch.Schema, edges=batch.Edges, config=config)
			Result.update(
				{key:ret})
		return Result
