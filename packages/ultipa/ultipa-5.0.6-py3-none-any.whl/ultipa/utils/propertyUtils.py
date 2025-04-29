# -*- coding: utf-8 -*-
# @Time    : 2023/1/16 11:06 AM
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : propertyUtils.py
from ultipa.structs.PropertyType import PropertyTypeStr
from ultipa.types import ULTIPA
from typing import List


def isBasePropertyType(type: PropertyTypeStr):
	'''
	Judge whether a data type is a base property type (not a list).

	Args:
		type:

	Returns:

	'''
	if type in [PropertyTypeStr.STRING,
				PropertyTypeStr.INT,
				PropertyTypeStr.INT64,
				PropertyTypeStr.UINT32,
				PropertyTypeStr.UINT64,
				PropertyTypeStr.FLOAT,
				PropertyTypeStr.DOUBLE,
				PropertyTypeStr.DATETIME,
				PropertyTypeStr.TIMESTAMP,
				PropertyTypeStr.TEXT]:
		return True
	return False


def getPropertyTypesDesc(type: PropertyTypeStr, subTypes: List[PropertyTypeStr]):
	'''
	Generate the format string a list type corresponds to.

	Args:
		type:

		subTypes:

	Returns:
		str[]
	'''
	if type == PropertyTypeStr.LIST:
		subType = subTypes[0]
		if isBasePropertyType(subType):
			return f"{subType}[]"
	if type == PropertyTypeStr.SET:
		subType = subTypes[0]
		if isBasePropertyType(subType):
			return f"set({subType})"
	return type
