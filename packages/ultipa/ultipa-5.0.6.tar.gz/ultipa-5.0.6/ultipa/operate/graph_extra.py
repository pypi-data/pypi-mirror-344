import time

import json
from typing import Tuple, List, Dict

from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.types.types_response import *
from ultipa.types import ULTIPA
from ultipa.types.types import Status, ErrorCode
from ultipa.types.types_response import Response
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertToGraph
from ultipa.structs.GraphSet import GraphSet
from ultipa.utils.noneCheck import checkNone

REPLACE_KEYS = {
	"graph": "name",
}


class GraphExtra(BaseExtra):
	'''
	Processing class that defines settings for GraphSet related operations.
	'''

	def showGraph(self, config: RequestConfig = RequestConfig()) ->List[GraphSet]:
		'''
		Args:
			config: An object of RequestConfig class

		Returns:
			List[GraphSet]
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraphMore, commonParams=config)
		uqlMaker.setCommandParams("")
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		if res.status.code == ULTIPA.ErrorCode.SUCCESS and  len(res.data) >0:
			res.data = convertToGraph(res)
		return res.data

	def getGraph(self, graphName: str,
				 config: RequestConfig = RequestConfig()) -> GraphSet:
		'''
		Args:
			graphName: The name of GraphSet

			config: An object of RequestConfig class

		Returns:
			GraphSet
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=config)
		uqlMaker.setCommandParams(graphName)
		uqlMaker.addParam(key='more',value=graphName)
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		if res.status.code == ULTIPA.ErrorCode.SUCCESS and len(res.data)>0:
			res.data = convertToGraph(res)
		else:
			res.data = None
		return res.data

	def createGraph(self, graphSet: GraphSet,
					config: RequestConfig = RequestConfig()) -> Response:
		'''
		Create a GraphSet.

		Args:
			graphSet: The graph to be created; the attribute name is mandatory, shards, partitionBy and description are optional.

			config: An object of RequestConfig class

		Returns:
			Response
		'''
		if checkNone(graphSet.name):
			return Response(status=Status(code = ErrorCode.PARAM_ERROR,message='The name of graphSet cannot be None'))
		shardslist = f" shards {[int(shard) if shard.isdigit() else 0 for shard in graphSet.shards]}" if isinstance(graphSet.shards,list) and len(graphSet.shards) >0 else ''
		partitionby = f" PARTITION BY HASH({graphSet.partitionBy})" if graphSet.partitionBy is not None else ''
		comment = f" COMMENT '{graphSet.description}'" if graphSet.description else ''
		gqlMaker = CommandList.createGraphGql + f"{graphSet.name} {{ }} {partitionby} {shardslist} {comment}"
		res = self.gql(gqlMaker,config = config)
		return res


	def dropGraph(self, graphName: str,
				  config: RequestConfig = RequestConfig()) -> Response:
		'''
		Drop a GraphSet.

		Args:
			graphName: The name of GraphSet

			config: An object of RequestConfig class

		Returns:
			Response
		'''

		uqlMaker = UQLMAKER(command=CommandList.dropGraph, commonParams=config)
		uqlMaker.setCommandParams(graphName)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterGraph(self, graphName: str, alterGraphSet: GraphSet,
			   config: RequestConfig = RequestConfig()) -> Response:
		'''
		Args:
			graphName: The orignal name of GraphSet

			alterGraphSet: A GraphSet object used to set the new name and/or description for the graph. the attribute name is mandatory

			config: An object of RequestConfig class

		Returns:
			Response
		'''
		if checkNone(alterGraphSet.name):
			return Response(status=Status(code=ErrorCode.PARAM_ERROR,message='The name of alterGraphSet cannot be None'))
		config.graph = graphName
		uqlMaker = UQLMAKER(command=CommandList.alterGraph, commonParams=config)
		uqlMaker.setCommandParams(graphName)
		data = {"name": alterGraphSet.name}
		if alterGraphSet.description is not None:
			data.update({'description': alterGraphSet.description})
		uqlMaker.addParam("set", data)
		res = self.uqlSingle(uqlMaker)
		return res

	def hasGraph(self, graphName: str, config: RequestConfig = RequestConfig()) -> bool:
		'''
		Check if graph exists or not.

		Args:
			graphName: The name of GraphSet

			config: An object of RequestConfig class

		Returns:
			bool
		'''

		graphsdata = self.showGraph(config)
		for graphs in graphsdata:
			if (graphs.name == graphName):
				return True

		return False

	def createGraphIfNotExist(self, graphSet: GraphSet,
							  config: RequestConfig = RequestConfig()) -> ResponseWithExistCheck:
		'''
		Checks if graph exists or not, if graph does not exist then creates new.

		Args:
			graphSet: The object of graphSet

			config: An object of RequestConfig class

		Returns:
			ResponseWithExistCheck
		'''

		if (self.hasGraph(graphSet.name, config)) == True:
			return ResponseWithExistCheck(exist=True,response=Response())

		else:
			res = self.createGraph(graphSet,config = config)
			return ResponseWithExistCheck(exist=False,response=res)
