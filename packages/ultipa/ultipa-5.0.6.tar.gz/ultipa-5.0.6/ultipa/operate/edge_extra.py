from ultipa import UpdateEdge
from ultipa.operate.base_extra import BaseExtra
from ultipa.types.types_response import *

from ultipa.types import  ULTIPA
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.InsertType import InsertType
from ultipa.configuration.InsertRequestConfig import InsertRequestConfig
from ultipa.structs.Edge import Edge
from ultipa.utils.noneCheck import checkNone
from ultipa.utils.ufilter.new_ufilter import *


class EdgeExtra(BaseExtra):
    '''
    Processing class that defines settings for edge related operations.

    '''
    def insertEdges(self, edges: List[Edge], schemaName: str,
                    config: InsertRequestConfig) -> Response:
        '''
        Insert edges.

        Args:
            edges: The list of edges to be inserted; the attributes fromId and toId of each Edge are mandatory, uuid, fromUuid, and toUuid cannot be set.

            schemaName: Name of the schema

            config: An object of InsertRequestConfig class

        Returns:
            Response
        '''
        combined_values = []  # to combine values and id for insertion
        for edge in edges:
            if checkNone(edge.fromId) or checkNone(edge.toId):
                return Response(status=Status(code = ErrorCode.PARAM_ERROR,message='The fromId and toId of edge cannot be None'))
            edge_dict = {}
            if edge.fromId:
                edge_dict["_from"] = edge.fromId
            if edge.toId:
                edge_dict["_to"] = edge.toId

            if edge.fromUuid:
                edge_dict["_from_uuid"] = edge.fromUuid
            if edge.toUuid:
                edge_dict["_to_uuid"] = edge.toUuid

            if edge.uuid:
                edge_dict["_uuid"] = edge.uuid
            edge_dict.update(edge.values)
            combined_values.append(edge_dict)
        edges = combined_values
        schemaName = '@' + schemaName

        uqlMaker = UQLMAKER(command=CommandList.insert, commonParams=config)
        if config.insertType == InsertType.UPSERT:
            uqlMaker = UQLMAKER(command=CommandList.upsert, commonParams=config)
        if config.insertType == InsertType.OVERWRITE:
            uqlMaker.addParam('overwrite', "", required=False)
        if schemaName:
            uqlMaker.addParam('into', schemaName, required=False)
        uqlMaker.addParam('edges', edges)

        if config.silent == False:
            uqlMaker.addParam('as', "edges")
            uqlMaker.addParam('return', "edges{*}")
        res = self.uqlSingle(uqlMaker)
        return res