
from ultipa import DBType
from ultipa.utils.convert import convertTableToDict
from ultipa.operate.base_extra import BaseExtra
from ultipa.utils import UQLMAKER, CommandList
from ultipa.types import ULTIPA_REQUEST, ULTIPA
from ultipa.types.types_response import *
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.utils.noneCheck import checkNone

JSONSTRING_KEYS = ["graph_privileges", "system_privileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class TruncateExtra(BaseExtra):
    '''
        Processing class that defines settings for advanced operations on graphset.
    '''

    def truncate(self,
                 params: ULTIPA_REQUEST.TruncateParams,
                 config: RequestConfig = RequestConfig()) -> Response:
        '''
        Truncate graphset.

        Args:
            params: The truncate parameters; the attribute graphName is mandatory, schemaName and dbType are optional while they must be set together.

            config: An object of RequestConfig class.

        Returns:
            Response

        '''

        if checkNone(params.graphName):
            return Response(Status(code=ULTIPA.ErrorCode.PARAM_ERROR,message='The graphName of params cannot be None'))
        else :
            if checkNone(params.dbType) and (not checkNone(params.schemaName) or params.schemaName =='*') :
                return Response(status=ULTIPA.Status(code = ULTIPA.ErrorCode.PARAM_ERROR,
                                                   message="The schemaName and dbType of params must be set together"))
        command = CommandList.truncate
        config.graph = params.graphName
        uqlMaker = UQLMAKER(command, commonParams=config)
        uqlMaker.addParam("graph", params.graphName)

        if params.dbType is not None:
            if params.dbType == DBType.DBNODE:
                if params.schemaName == "*" or params.schemaName is None:
                    uqlMaker.addParam("nodes", "*")
                else:
                    uqlMaker.addParam("nodes", "@" + params.schemaName, notQuotes=True)
            if params.dbType == DBType.DBEDGE:
                if params.schemaName == "*" or params.schemaName is None:
                    uqlMaker.addParam("edges", "*")
                else:
                    uqlMaker.addParam("edges", "@" + params.schemaName, notQuotes=True)

        return self.uqlSingle(uqlMaker)

    def compact(self, graphName: str,
                config: RequestConfig = RequestConfig()) -> JobResponse:
        '''
        Compact graphshet.

        Args:
            graphName: The name of graphset

            config: An object of RequestConfig class

        Returns:
            JobResponse

        '''
        command = CommandList.compact
        uqlMaker = UQLMAKER(command, commonParams=config)
        uqlMaker.addParam("graph", graphName)
        result = self.uqlSingle(uqlMaker)
        jobResponse = JobResponse()
        jobResponse.statistics = result.statistics
        jobResponse.status = result.status
        if result.items:
            res = convertTableToDict(result.alias(result.aliases[0].name).entities.rows, result.alias(result.aliases[0].name).entities.headers)

            jobResponse.jobId = res[0]['new_job_id']
            return jobResponse
        else:
            return jobResponse
