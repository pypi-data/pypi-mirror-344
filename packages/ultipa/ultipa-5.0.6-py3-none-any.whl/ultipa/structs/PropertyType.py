# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:40
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : PropertyType.py
from enum import Enum

from ultipa.proto import ultipa_pb2


class PropertyTypeStr:
    '''
        Data class for property type mapping to string.
    '''
    INT = 'int32'
    STRING = 'string'
    FLOAT = 'float'
    DOUBLE = 'double'
    UINT32 = 'uint32'
    INT64 = 'int64'
    UINT64 = 'uint64'
    DATETIME = 'datetime'
    TIMESTAMP = 'timestamp'
    TEXT = 'text'
    BLOB = "blob"
    BOOL = "bool"
    UNSET = "unset"
    POINT = "point"
    LIST = "list"
    SET = "set"
    MAP = "map"
    BLOB = "blob"


class UltipaPropertyType(Enum):
    '''
        Data class for property type mapping to gRPC.
    '''
    UNSET = ultipa_pb2.UNSET
    INT32 = ultipa_pb2.INT32
    STRING = ultipa_pb2.STRING
    FLOAT = ultipa_pb2.FLOAT
    DOUBLE = ultipa_pb2.DOUBLE
    UINT32 = ultipa_pb2.UINT32
    INT64 = ultipa_pb2.INT64
    UINT64 = ultipa_pb2.UINT64
    DATETIME = ultipa_pb2.DATETIME
    TIMESTAMP = ultipa_pb2.TIMESTAMP
    TEXT = ultipa_pb2.TEXT
    BLOB = ultipa_pb2.BLOB
    BOOL = ultipa_pb2.BOOL
    POINT = ultipa_pb2.POINT
    DECIMAL = ultipa_pb2.DECIMAL
    LIST = ultipa_pb2.LIST
    SET = ultipa_pb2.SET
    MAP = ultipa_pb2.MAP
    NULL = ultipa_pb2.NULL_
    ID = -1
    UUID = -2
    FROM = -3
    TO = -4
    FROM_UUID = -5
    TO_UUID = -6
    IGNORE = -7


