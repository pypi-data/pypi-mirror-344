# -*- coding: utf-8 -*-
# @Time    : 2023/1/17 9:45 AM
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : null.py
import sys
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils.errors import ParameterException, ServerException, SerializeException, checkError


StringNull = bytes([0x00])
Int32Null = bytes([0x7f,0xff,0xff,0xff])
Uint32Null =bytes([0xff,0xff,0xff,0xff])
Int64Null = bytes([0x7f,0xff,0xff,0xff,0xff,0xff,0xff,0xff])
Uint64Null = bytes([0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff])
FloatNull = bytes([0xff,0xff,0xff,0xff])
DoubleNull = bytes([0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff])
PointNull = bytes([0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff])
BoolNull = bytes([0x2])

def nullValue(type:ULTIPA.UltipaPropertyType):
	'''
	Returns the null value corresponding to different data types

	Args:
		type: The data type

	Returns:

	'''
	if type in [ULTIPA.UltipaPropertyType.STRING.value,ULTIPA.UltipaPropertyType.TEXT.value,ULTIPA.UltipaPropertyType.BLOB.value,ULTIPA.UltipaPropertyType.DECIMAL.value]:
		return StringNull
	elif type == ULTIPA.UltipaPropertyType.INT32.value:
		return Int32Null
	elif type == ULTIPA.UltipaPropertyType.UINT32.value:
		return Uint32Null
	elif type == ULTIPA.UltipaPropertyType.INT64.value:
		return Int64Null
	elif type == ULTIPA.UltipaPropertyType.UINT64.value:
		return Uint64Null
	elif type == ULTIPA.UltipaPropertyType.FLOAT.value:
		return FloatNull
	elif type == ULTIPA.UltipaPropertyType.DOUBLE.value:
		return DoubleNull
	elif type == ULTIPA.UltipaPropertyType.DATETIME.value:
		return Uint64Null
	elif type == ULTIPA.UltipaPropertyType.TIMESTAMP.value:
		return Uint32Null
	elif type == ULTIPA.UltipaPropertyType.POINT.value:
		return PointNull
	elif type == ULTIPA.UltipaPropertyType.BOOL.value:
		return BoolNull
	elif type in [ULTIPA.UltipaPropertyType.LIST.value,ULTIPA.UltipaPropertyType.SET.value]:
		return None
	raise SerializeException(f"not support [{ULTIPA.Property._PropertyReverseMap.get(type)}]")

def isNullValue(v: any, type:ULTIPA.UltipaPropertyType):
	'''
	Judge whether a value is null

	Args:
		v: The value to be judged
		type: The property type of v

	Returns:
		bool

	'''
	try:
		nullV = nullValue(type)
		return nullV == v
	except Exception as e:
		raise SerializeException(e)
	return False






if __name__ == '__main__':
	print(sys.float_info.max)
	print(sys.int_info)
	print("Int32Null：",Int32Null)
	print("Ret：",0X7FFFFFFF==Int32Null)
	print("Uint32Null：",Uint32Null)
	print("Int64Null：",Int64Null)
	print("Uint64Null：",Uint64Null)
	print("FloatNull：",FloatNull)
	print("DoubleNull：",DoubleNull)
