# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 14:46
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Property.py
from typing import List, Dict

from ultipa.utils.noneCheck import checkNone

from ultipa.structs.BaseModel import BaseModel
from ultipa.structs.PropertyType import UltipaPropertyType


class DecimalExtra:
    def __init__(self, precision: int = 0, scale: int = 0):
        self.precision = precision
        self.scale = scale


class Property(BaseModel):
    '''
        Data class for property.
    '''

    @staticmethod
    def decimalExtra(precision, scale):
        precision = precision if not checkNone(precision) else 0
        scale = scale if not checkNone(scale) else 0
        return f"{precision},{scale}"

    def __init__(self,
                 name: str = None,
                 type: UltipaPropertyType = None,
                 subType: List[UltipaPropertyType] = None,
                 lte: bool = None,
                 read: bool = None,
                 write: bool = None,
                 schema: str = None,
                 description: str = None,
                 encrypt: str = None,
                 decimalExtra : DecimalExtra = None
                 ):
        self.type = type
        self.subType = subType
        self.description = description
        self.name = name
        self.lte = lte
        self.schema = schema
        self.encrypt = encrypt
        self.decimalExtra  = Property.decimalExtra(decimalExtra .precision,decimalExtra .precision) if not checkNone(decimalExtra )  else None
        self.read = read
        self.write = write

    _PropertyMap = {
        "string": UltipaPropertyType.STRING,
        "int32": UltipaPropertyType.INT32,
        "int64": UltipaPropertyType.INT64,
        "uint32": UltipaPropertyType.UINT32,
        "uint64": UltipaPropertyType.UINT64,
        "float": UltipaPropertyType.FLOAT,
        "double": UltipaPropertyType.DOUBLE,
        "datetime": UltipaPropertyType.DATETIME,
        "timestamp": UltipaPropertyType.TIMESTAMP,
        "text": UltipaPropertyType.TEXT,
        "blob": UltipaPropertyType.BLOB,
        "_id": UltipaPropertyType.ID,
        "_uuid": UltipaPropertyType.UUID,
        "_from": UltipaPropertyType.FROM,
        "_to": UltipaPropertyType.TO,
        "_from_uuid": UltipaPropertyType.FROM_UUID,
        "_to_uuid": UltipaPropertyType.TO_UUID,
        "_ignore": UltipaPropertyType.IGNORE,
        "unset": UltipaPropertyType.UNSET,
        "point": UltipaPropertyType.POINT,
        "decimal": UltipaPropertyType.DECIMAL,
        "list": UltipaPropertyType.LIST,
        "set": UltipaPropertyType.SET,
        "map": UltipaPropertyType.MAP,
        "null": UltipaPropertyType.NULL,
        "bool": UltipaPropertyType.BOOL
    }

    _PropertyReverseMap = {
        UltipaPropertyType.STRING: "string",
        UltipaPropertyType.INT32: "int32",
        UltipaPropertyType.INT64: "int64",
        UltipaPropertyType.UINT32: "uint32",
        UltipaPropertyType.UINT64: "uint64",
        UltipaPropertyType.FLOAT: "float",
        UltipaPropertyType.DOUBLE: "double",
        UltipaPropertyType.DATETIME: "datetime",
        UltipaPropertyType.TIMESTAMP: "timestamp",
        UltipaPropertyType.TEXT: "text",
        UltipaPropertyType.BLOB: "blob",
        UltipaPropertyType.ID: "_id",
        UltipaPropertyType.UUID: "_uuid",
        UltipaPropertyType.FROM: "_from",
        UltipaPropertyType.TO: "_to",
        UltipaPropertyType.FROM_UUID: "_from_uuid",
        UltipaPropertyType.TO_UUID: "_to_uuid",
        UltipaPropertyType.IGNORE: "_ignore",
        UltipaPropertyType.UNSET: "unset",
        UltipaPropertyType.POINT: "point",
        UltipaPropertyType.DECIMAL: "decimal",
        UltipaPropertyType.LIST: "list",
        UltipaPropertyType.SET: "set",
        UltipaPropertyType.MAP: "map",
        UltipaPropertyType.NULL: "null",
        UltipaPropertyType.BOOL: "bool",
    }

    _PropertyEnumMap = {
        UltipaPropertyType.STRING.value: UltipaPropertyType.STRING,
        UltipaPropertyType.INT32.value: UltipaPropertyType.INT32,
        UltipaPropertyType.INT64.value: UltipaPropertyType.INT64,
        UltipaPropertyType.UINT32.value: UltipaPropertyType.UINT32,
        UltipaPropertyType.UINT64.value: UltipaPropertyType.UINT64,
        UltipaPropertyType.FLOAT.value: UltipaPropertyType.FLOAT,
        UltipaPropertyType.DOUBLE.value: UltipaPropertyType.DOUBLE,
        UltipaPropertyType.DATETIME.value: UltipaPropertyType.DATETIME,
        UltipaPropertyType.TIMESTAMP.value: UltipaPropertyType.TIMESTAMP,
        UltipaPropertyType.TEXT.value: UltipaPropertyType.TEXT,
        UltipaPropertyType.BLOB.value: UltipaPropertyType.BLOB,
        UltipaPropertyType.ID.value: UltipaPropertyType.ID,
        UltipaPropertyType.UUID.value: UltipaPropertyType.UUID,
        UltipaPropertyType.FROM.value: UltipaPropertyType.FROM,
        UltipaPropertyType.TO.value: UltipaPropertyType.TO,
        UltipaPropertyType.FROM_UUID.value: UltipaPropertyType.FROM_UUID,
        UltipaPropertyType.TO_UUID.value: UltipaPropertyType.TO_UUID,
        UltipaPropertyType.IGNORE.value: UltipaPropertyType.IGNORE,
        UltipaPropertyType.UNSET.value: UltipaPropertyType.UNSET,
        UltipaPropertyType.POINT.value: UltipaPropertyType.POINT,
        UltipaPropertyType.DECIMAL.value: UltipaPropertyType.DECIMAL,
        UltipaPropertyType.LIST.value: UltipaPropertyType.LIST,
        UltipaPropertyType.SET.value: UltipaPropertyType.SET,
        UltipaPropertyType.MAP.value: UltipaPropertyType.MAP,
        UltipaPropertyType.NULL.value: UltipaPropertyType.NULL,
        UltipaPropertyType.BOOL.value: UltipaPropertyType.BOOL
    }

    def setSubTypesbyType(self, type: str):
        if "string" in type:
            self.subType = [UltipaPropertyType.STRING]

        if "int32" in type:
            self.subType = [UltipaPropertyType.INT32]

        if "uint32" in type:
            self.subType = [UltipaPropertyType.UINT32]

        if "int64" in type:
            self.subType = [UltipaPropertyType.INT64]

        if "uint64" in type:
            self.subType = [UltipaPropertyType.UINT64]

        if "float" in type:
            self.subType = [UltipaPropertyType.FLOAT]

        if "double" in type:
            self.subType = [UltipaPropertyType.DOUBLE]

        if "datetime" in type:
            self.subType = [UltipaPropertyType.DATETIME]

        if "timestamp" in type:
            self.subType = [UltipaPropertyType.TIMESTAMP]

        if "text" in type:
            self.subType = [UltipaPropertyType.TEXT]

    def isIdType(self) -> bool:
        idTypes = [
            UltipaPropertyType.ID.value,
            UltipaPropertyType.TO.value,
            UltipaPropertyType.UUID.value,
            UltipaPropertyType.FROM.value,
            UltipaPropertyType.FROM_UUID.value,
            UltipaPropertyType.TO_UUID.value,
        ]
        idTypesEnum = [
            UltipaPropertyType.ID,
            UltipaPropertyType.TO,
            UltipaPropertyType.UUID,
            UltipaPropertyType.FROM,
            UltipaPropertyType.FROM_UUID,
            UltipaPropertyType.TO_UUID,
        ]
        return self.type in idTypes or self.type in idTypesEnum

    def isIgnore(self):
        return self.type == UltipaPropertyType.IGNORE.value

    def setTypeStr(self, value):
        self.type = self.getStringByPropertyType(value)

    def setTypeInt(self, value):
        self.type = self.getPropertyTypeByString(value)

    def getStringType(self):
        return self.getStringByPropertyType(self.type)

    def getPropertyTypeByString(self, v):
        if isinstance(v, str) and 'decimal' in v:
            self.decimalExtra  = v
            v = 'decimal'
        if not self._PropertyMap.get(v):
            if not self._PropertyReverseMap.get(v):
                if "[" in v:
                    self.setSubTypesbyType(v)
                    return UltipaPropertyType.LIST
                if '<' in v:
                    self.setSubTypesbyType(v)
                    return UltipaPropertyType.SET
            else:
                return v

        return self._PropertyMap.get(v)

    def getStringByPropertyType(self, v):
        if v == UltipaPropertyType.DECIMAL:
            return f'decimal({self.decimalExtra })'
        if isinstance(v, str):
            return v
        return self._PropertyReverseMap[v]

    @staticmethod
    def getPropertyByInt(v):
        if v:
            return Property._PropertyEnumMap[v]
        return v

    @staticmethod
    def _getStringByPropertyType(v):
        return Property._PropertyReverseMap[Property.getPropertyByInt(v)]

    @staticmethod
    def _getPropertyTypeByString(v):
        return Property._PropertyMap.get(v)
