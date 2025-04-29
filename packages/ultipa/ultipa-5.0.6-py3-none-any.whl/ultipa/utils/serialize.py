import datetime
import math

from ultipa.proto.ultipa_pb2 import ListData, SetData, AttrListData
from ultipa.structs import Property
from ultipa.types import ULTIPA
from struct import *

from ultipa.utils import nullValue
from ultipa.utils.common import DateTimeIs2Str, Float_Accuracy, TimestampIs2Str
from ultipa.utils.ultipa_datetime import UltipaDatetime
from ultipa.utils.errors import ParameterException, ServerException, SerializeException, checkError
import ast

class _Serialize:
	'''
	Configuration class that defines settings for serialization.
	'''
	def __init__(self, type, value, name=None, export=False, timeZoneOffset=None, subTypes=None, timeZone=None):
		self.type = type
		self.value = value
		self.subTypes = subTypes
		self.name = name
		self.export = export
		self.timeZoneOffset = timeZoneOffset
		self.timeZone = timeZone

	def serialize(self):
		if self.value is None and not self.subTypes:
			self.value = nullValue.nullValue(self.type)
			return self.value

		# if self.value is None:
		# 	self.value = nullValue.nullValue(self.type)
		# 	return self.value
		if self.type == ULTIPA.UltipaPropertyType.BLOB.value:
			return str(self.value).encode()

		if self.type == ULTIPA.UltipaPropertyType.STRING.value or self.type == ULTIPA.UltipaPropertyType.TEXT.value or self.type == ULTIPA.UltipaPropertyType.POINT.value or self.type == ULTIPA.UltipaPropertyType.DECIMAL.value:
			if isinstance(self.value, str):
				return self.value.encode()
			elif isinstance(self.value, bytes):
				return self.value
			else:
				return str(self.value).encode()

		elif self.type == ULTIPA.UltipaPropertyType.BOOL.value:
			return str(int(self.value)).encode()

		elif self.type == ULTIPA.UltipaPropertyType.INT32.value:
			if self.value == '':
				self.value = 0
			try:
				upret = pack('>i', int(self.value))
				return upret
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")

		elif self.type == ULTIPA.UltipaPropertyType.UINT32.value:
			if self.value == '':
				self.value = 0
			try:
				upret = pack('>I', int(self.value))
				return upret
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")

		elif self.type == ULTIPA.UltipaPropertyType.INT64.value:
			if self.value == '':
				self.value = 0
			try:
				upret = pack('>q', int(self.value))
				return upret
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")


		elif self.type == ULTIPA.UltipaPropertyType.UINT64.value:
			if self.value == '':
				self.value = 0
			try:
				upret = pack('>Q', int(self.value))
				return upret
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")

		elif self.type == ULTIPA.UltipaPropertyType.FLOAT.value:
			if self.value == '':
				self.value = 0

			try:
				upret = pack('>f', self.value)
				return upret
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")

		elif self.type == ULTIPA.UltipaPropertyType.DOUBLE.value:
			if self.value == '':
				self.value = 0
			try:
				upret = pack('>d', self.value)
				return upret
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")

		elif self.type == ULTIPA.UltipaPropertyType.DATETIME.value:
			if self.value is None:
				self.value = 0
			else:
				self.value = UltipaDatetime.datetimeStr2datetimeInt(self.value)
			try:
				upret = pack('>Q', self.value)
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")
			return upret

		elif self.type == ULTIPA.UltipaPropertyType.TIMESTAMP.value:
			if self.value is None:
				self.value = 0
			else:
				if isinstance(self.value, datetime.datetime):
					self.value = int(self.value.timestamp())
				if isinstance(self.value, str):
					self.value = UltipaDatetime.timestampStr2timestampInt(self.value, self.timeZone,
																		  self.timeZoneOffset)
			try:
				upret = pack('>I', self.value)
				return upret
			except Exception as e:
				error = checkError(e.args[0])
				raise SerializeException(err=f"property [%s],value=%s {error}")

		elif (self.type == ULTIPA.UltipaPropertyType.LIST.value or self.type == ULTIPA.UltipaPropertyType.SET.value)and self.subTypes != None and len(self.subTypes) > 0:
			listData = ListData()
			if self.value == None:
				listData.is_null = True
				self.value = []
			for i, v in enumerate(self.value):
				if isinstance(self.subTypes[0],str):
					type = Property._getPropertyTypeByString(self.subTypes[0]).value
				else:
					type = self.subTypes[0]
				listData.values.append(_Serialize(type, v, timeZone=self.timeZone,
										  timeZoneOffset=self.timeZoneOffset).serialize())
			return listData.SerializeToString()


		elif self.type == ULTIPA.UltipaPropertyType.MAP.value and self.subTypes != None and len(self.subTypes) > 0:
			setData = SetData()
			if self.value == None:
				setData.is_null = True
				self.value = set()
			for i, v in enumerate(self.value):
				setData.values.add(_Serialize(self.subTypes[0], v).serialize())
			return setData.SerializeToString()

	def unserialize(self):
		try:
			if self.type == ULTIPA.UltipaPropertyType.NULL.value:
				return None

			if nullValue.isNullValue(self.value, self.type):
				return None

			elif self.type == ULTIPA.UltipaPropertyType.BLOB.value:
				return list(bytearray(self.value))

			elif self.type == ULTIPA.UltipaPropertyType.STRING.value or self.type == ULTIPA.UltipaPropertyType.DECIMAL.value or self.type == ULTIPA.UltipaPropertyType.TEXT.value or type is None:
				return self.value.decode()

			elif self.type == ULTIPA.UltipaPropertyType.BOOL.value:
				return self.value.decode()=="1"

			elif self.type == ULTIPA.UltipaPropertyType.POINT.value:
				if len(self.value) != 16:
					raise ParameterException("deserialize point type error: length != 16")
				latitude_v = self.value[:8]
				latitude = self.unpackDouble(latitude_v)

				longitude_v = self.value[8:16]
				longitude = self.unpackDouble(longitude_v)
				if math.isnan(longitude) or math.isnan(latitude):
					return None
				return f"POINT({latitude} {longitude})"



			elif self.type == ULTIPA.UltipaPropertyType.INT32.value:
				if len(self.value) >= 4:
					ls = len(self.value) // 4 * 'i' or 'i'
				elif len(self.value) == 2:
					ls = len(self.value) // 2 * 'h' or 'h'
				else:
					ls = 'h'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.UINT32.value:
				ls = len(self.value) // 4 * 'I' or 'I'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.INT64.value:
				ls = len(self.value) // 8 * 'q' or 'q'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.UINT64.value:
				ls = len(self.value) // 8 * 'Q' or 'Q'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.FLOAT.value:
				ls = len(self.value) // 4 * 'f' or 'f'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				if Float_Accuracy:
					return round(ret, 7)
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.DOUBLE.value:
				ls = len(self.value) // 8 * 'd' or 'd'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.DATETIME.value:
				ls = len(self.value) // 8 * 'Q' or 'Q'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				if DateTimeIs2Str:
					ret = UltipaDatetime.datetimeInt2datetimeStr(ret)
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.TIMESTAMP.value:
				ls = len(self.value) // 4 * 'I' or 'I'
				upret = unpack(f'>{ls}', self.value)
				ret = upret[0]
				if TimestampIs2Str:
					ret = UltipaDatetime.timestampInt2timestampStr(ret, self.timeZone, self.timeZoneOffset)
				if nullValue.isNullValue(self.value, self.type):
					return None
				return ret
			elif self.type == ULTIPA.UltipaPropertyType.LIST.value and self.subTypes != None and len(self.subTypes) > 0:
				ret = []
				listData = ListData()
				listData.ParseFromString(self.value)
				if listData.is_null == True:
					return None
				for v in listData.values:
					ret.append(_Serialize(self.subTypes[0], v, timeZone=self.timeZone,
										  timeZoneOffset=self.timeZoneOffset).unserialize())
				return ret

			elif self.type == ULTIPA.UltipaPropertyType.SET.value:
				ret = set()
				setData = SetData()
				setData.ParseFromString(self.value)
				if setData.is_null == True:
					return None
				for value in setData.values:
					ret.add(_Serialize(self.subTypes[0], value, timeZone=self.timeZone,
										  timeZoneOffset=self.timeZoneOffset).unserialize())
				return list(ret)
				# ret = ast.literal_eval(self.value.decode("utf-8"))
				# return ret
			else:
				raise ServerException('Server returned type error')

		except Exception as e:
			raise ParameterException(err=e)

	def packDouble(self,value):
		return pack('>d', value)

	def unpackDouble(self,value):
		ls = len(value) // 8 * 'd' or 'd'
		upret = unpack(f'>{ls}', value)
		latitude = upret[0]
		return latitude


	def setDefaultValue(self):
		if self.type == ULTIPA.UltipaPropertyType.STRING.value:
			self.value = ""
			return
		elif self.type == ULTIPA.UltipaPropertyType.INT32.value:
			self.value = 0
			return
		elif self.type == ULTIPA.UltipaPropertyType.UINT32.value:
			self.value = 0
			return
		elif self.type == ULTIPA.UltipaPropertyType.INT64.value:
			self.value = 0
			return
		elif self.type == ULTIPA.UltipaPropertyType.UINT64.value:
			self.value = 0
			return
		elif self.type == ULTIPA.UltipaPropertyType.FLOAT.value:
			self.value = 0
			return
		elif self.type == ULTIPA.UltipaPropertyType.DOUBLE.value:
			self.value = 0
			return
		elif self.type == ULTIPA.UltipaPropertyType.TEXT.value:
			self.value = ""
			return
		elif self.type == ULTIPA.UltipaPropertyType.DATETIME.value:
			self.value = "1970-01-01"
			return
		elif self.type == ULTIPA.UltipaPropertyType.TIMESTAMP.value:
			self.value = "1970-01-01"
			return
