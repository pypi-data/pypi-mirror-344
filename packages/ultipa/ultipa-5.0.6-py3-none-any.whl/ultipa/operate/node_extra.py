from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA
from ultipa.types.types_response import *
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.InsertType import InsertType
from ultipa.configuration.InsertRequestConfig import InsertRequestConfig
from ultipa.structs.Node import Node
from ultipa.utils.ufilter.new_ufilter import *

class NodeExtra(BaseExtra):
	'''
	Processing class that defines settings for node related operations.

	'''
	def insertNodes(self, nodes: List[Node], schemaName: str, config:InsertRequestConfig) -> Response:
		'''
		Insert nodes.

		Args:
			nodes: List of nodes to be inserted

			schemaName: The name of the Schema

			config: An object of InsertConfig class

		Returns:
			Response
		'''

		combined_values = []
		for node in nodes:
			node_dict = {}
			if node.id:
				node_dict['_id'] = node.id
			node_dict.update(node.values)
			combined_values.append(node_dict)

		nodes=combined_values
		schemaName='@' + schemaName

		uqlMaker = UQLMAKER(command=CommandList.insert, commonParams=config)
		if config.insertType==InsertType.UPSERT:
			uqlMaker = UQLMAKER(command=CommandList.upsert, commonParams=config)
		if config.insertType==InsertType.OVERWRITE:
			uqlMaker.addParam('overwrite', "", required=False)
		if schemaName:
			uqlMaker.addParam('into', schemaName, required=False)

		uqlMaker.addParam('nodes', nodes)

		if config.silent==False:
			uqlMaker.addParam('as', "nodes")
			uqlMaker.addParam('return', "nodes{*}")

		res = self.uqlSingle(uqlMaker)
		return res

