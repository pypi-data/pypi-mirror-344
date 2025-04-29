from ultipa import DBType, UltipaPropertyType
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.types.types_response import *
from ultipa.types.types import Status, ErrorCode
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.noneCheck import checkNone
from ultipa.utils.propertyUtils import getPropertyTypesDesc
from typing import Tuple, List, Dict

BOOL_KEYS = ["index", "lte"]
REPLACE_KEYS = {
    "name": "propertyName",
    "type": "propertyType",
}


class PropertyExtra(BaseExtra):
    '''
    Processing class that defines settings for property related operations.
    '''

    def showProperty(self, dbType: DBType = None, schemaName: str = None,
                     config: RequestConfig = RequestConfig()) -> Dict[str, List[Property]]:
        '''
        Show all Node or Edge Schema properties.

        Args:
            dbType: The DBType of data (DBNODE or DBEDGE)

            schemaName: The name of schema

            config: An object of RequestConfig class

        Returns:
            Dict[str, List[Property]]

        '''
        if not checkNone(schemaName) and (dbType == None or dbType == DBType.DBGLOBAL):
            return Response(status=Status(code=ErrorCode.PARAM_ERROR, message='When schemaName is not None , dbType cannot be None and DBGLOBAL'))
        if dbType == None or dbType == DBType.DBGLOBAL:

            command = CommandList.showProperty
            commandp = ''
        else:
            if dbType == DBType.DBNODE:
                command = CommandList.showNodeProperty
            elif dbType == DBType.DBEDGE:
                command = CommandList.showEdgeProperty
            else:
                raise TypeError("dbType must be an instance of DBType.DBNODE or DBType.DBEDGE or DBType.DBGLOBAL")
            if schemaName:
                commandp = ['@' + f"`{schemaName}`"]
            else:
                commandp = ''

        uqlMaker = UQLMAKER(command=command, commonParams=config)
        uqlMaker.setCommandParams(commandP=commandp)
        res = self.uqlSingle(uqlMaker=uqlMaker)
        propertyDict = {}
        nodeProperty = res.alias('_nodeProperty').asProperties()
        edgeProeprty = res.alias('_edgeProperty').asProperties()
        if nodeProperty :
            propertyDict['nodeProperties'] = nodeProperty
        if edgeProeprty :
            propertyDict['edgeProperties'] = edgeProeprty

        resprop = propertyDict['nodeProperties'] if dbType == DBType.DBNODE and 'nodeProperties' in propertyDict \
            else  propertyDict['edgeProperties'] if dbType == DBType.DBEDGE and 'edgeProperties' in propertyDict else propertyDict

        return resprop

    def showNodeProperty(self, schemaName: str = None,
                         config: RequestConfig = RequestConfig()) -> List[Property]:
        '''
        Show all Node Schema properties.

        Args:
            schemaName: The name of schema

            config: An object of RequestConfig class

        Returns:
            List[Property]

        '''
        res = self.showProperty(schemaName=schemaName, dbType=DBType.DBNODE, config=config)
        res = res if res else None
        return res

    def showEdgeProperty(self, schemaName: str = None,
                         config: RequestConfig = RequestConfig()) -> List[Property]:
        '''
        Show all Edge Schema properties.

        Args:
            schemaName: The name of schema

            config: An object of RequestConfig class

        Returns:
            List[Property]

        '''

        res = self.showProperty(schemaName=schemaName, dbType=DBType.DBEDGE, config=config)
        res = res if res else None
        return res

    def createProperty(self, dbType: DBType, property: Property,
                       config: RequestConfig = RequestConfig()) -> Response:
        '''
        Create a property.

        Args:
            dbType: The DBType of data (DBNODE or DBEDGE)

            property:   The property to be created; the attributes name and type (and subType if the type is SET or LIST) are mandatory, encrypt and description are optional.

            config: An object of RequestConfig class

        Returns:
            Response

        '''
        if not isinstance(property,Property) :
            message = 'property cannot None' if property is None else 'property type exception'
            return Response(status=Status(code=ErrorCode.FAILED, message=message))
        if (property.type == UltipaPropertyType.LIST or property.type == UltipaPropertyType.SET) and checkNone(
                property.subType):
            return Response(status=Status(code=ErrorCode.PARAM_ERROR, message='if the type is SET or LIST,The subType of property cannot be None'))
        if checkNone(property.schema) or checkNone(property.type) :
            message = checkNone(property.schema) and 'The schema of property cannot be None' or 'The type of property cannot be None'
            return Response(status=Status(code=ErrorCode.PARAM_ERROR, message=message))
        if checkNone(property.name):
            return Response(status=Status(code=ErrorCode.PARAM_ERROR, message='The name of property cannot be None'))
        if dbType == DBType.DBGLOBAL or checkNone(dbType):
            message = dbType == DBType.DBGLOBAL and 'The dbType cannot be DBType.DBGLOBAL' or 'The dbType cannot be None'
            return Response(status=Status(code=ErrorCode.PARAM_ERROR, message=message))
        command = dbType == DBType.DBNODE and CommandList.createNodeProperty or CommandList.createEdgeProperty
        property.type = property.getStringByPropertyType(property.type)
        if property.subType and isinstance(property.subType,list):
            property.subType = [property.getStringByPropertyType(property.subType[0])]
        commandP = ["@" + f"`{property.schema}`", f"`{property.name}`",
                    getPropertyTypesDesc(property.type, property.subType)]

        if property.description:
            commandP.append(property.description)

        uqlMaker = UQLMAKER(command=command, commonParams=config)
        uqlMaker.setCommandParams(commandP=commandP)
        if property.encrypt is not None:
            uqlMaker.addParam('encrypt',property.encrypt,required=False )
        res = self.uqlSingle(uqlMaker)
        return res

    def dropProperty(self, dbType: DBType, property:Property,
                     config: RequestConfig = RequestConfig()) -> Response:
        '''
        Drop a property.

        Args:
            dbType: The DBType of data (DBNODE or DBEDGE)

            property: An object of Property class

            config: An object of config class

        Returns:
            Response

        '''
        if checkNone(property.schema) :
            return Response(status=Status(code=ErrorCode.PARAM_ERROR,message='The shcema of property cannot be None'))
        schemaName = '*' if property.schema == '' or property.schema is None else property.schema
        command = dbType == DBType.DBNODE and CommandList.dropNodeProperty or CommandList.dropEdgeProperty
        commandP = "@`%s`.`%s`" % (schemaName, property.name)
        uqlMaker = UQLMAKER(command=command, commonParams=config)
        uqlMaker.setCommandParams(commandP=commandP)
        res = self.uqlSingle(uqlMaker)
        return res

    def alterProperty(self, dbType: DBType, originProp: Property, newProp: Property,
                      config: RequestConfig = RequestConfig()) -> Response:
        '''
        Alter a property.

        Args:
            dbType: The DBType of data (DBNODE or DBEDGE)

            originProp: The property to be altered; the attributes name and schema (writes * to specify all schemas) are mandatory.

            newProp: A Property object used to set the new name and/or description for the property.

            config: An object of RequestConfig class

        Returns:
            Response

        '''
        if checkNone(originProp.name) or checkNone(originProp.schema) :
            message = checkNone(originProp.name) and 'The name of originProp cannot be None' or 'The schema of originProp cannot be None'
            return Response(status=Status(code = ErrorCode.PARAM_ERROR,message = message))
        command = dbType == DBType.DBNODE and CommandList.alterNodeProperty or CommandList.alterEdgeProperty
        commandP = "@`%s`.`%s`" % (originProp.schema, originProp.name)
        update_dict = {}
        if newProp.name:
            update_dict.setdefault('name', newProp.name)
        if newProp.description:
            update_dict.update({'description': newProp.description})
        uqlMaker = UQLMAKER(command=command, commonParams=config)
        uqlMaker.setCommandParams(commandP)
        uqlMaker.addParam("set", update_dict)
        res = self.uqlSingle(uqlMaker)
        return res

