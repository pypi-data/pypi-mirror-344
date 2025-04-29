# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 18:14
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : InsertRequestConfig.py
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.InsertType import InsertType


class InsertRequestConfig(RequestConfig):
	'''
    Configuration class for the interface of insert operation.

    This class provides settings for inserting metadata.
    
    Args:
        - insertType (InsertType): The insertion mode. Supports NORMAL, UPSERT, and OVERWRITE.
        - graph (str):Name of the graph to use. If not specified, the graph defined in UltipaConfig.defaultGraph will be used.
        - timeout (int): Request timeout threshold (in second).
        - host (str): Specifies a host in a database cluster to execute the request.
        - timeZone (str): The string of timezone in standard format
        - timeZoneOffset (any): 1, the number of seconds; 2, a 5-character string such as +0700, -0430
        - silent (bool):Whether to return the _id or _uuid of the operated nodes or edges. Sets to Ture to not return, and False to return.
	'''
	def __init__(self,
				 insertType: InsertType = InsertType.NORMAL,
				 graph: str = '',
				 timeout: int = None,
				 host: str = None,
				 timeZone:str =None,
				 thread:int = None,
				 timeZoneOffset:int =None,
				 silent :bool = True):
		super().__init__(graph, timeout, host,thread, timeZone=timeZone,
						 timeZoneOffset=timeZoneOffset)
		self.insertType = insertType

		self.silent = silent

