import datetime
import re
import time
from dateutil.parser import parse
from ultipa.utils import errors
from ultipa.utils.errors import ParameterException


class UTC(datetime.tzinfo):
	def __init__(self, offsetHours=0, offsetSeconds=0):
		if offsetSeconds is None:
			self.__offset = 0
		else:
			self.__offset = offsetSeconds
		self.__offsetHour = offsetHours

	def utcoffset(self, dt):
		return datetime.timedelta(seconds=self.__offset, hours=self.__offsetHour)

	def tzname(self, dt):
		return 'UTC+%s dt: %s' % (self.__offsetHour, [dt, id(dt)])

	def dst(self, dt):
		return datetime.timedelta(seconds=self.__offset, hours=self.__offsetHour)

def getTimeZoneSeconds(timeZone):
	import pytz
	try:
		tz = pytz.timezone(timeZone)
		utc_offset = tz.utcoffset(datetime.datetime.utcnow())
		return utc_offset.total_seconds()
	except pytz.exceptions.UnknownTimeZoneError as e:
		raise errors.ParameterException("UnknownTimeZoneError:" + str(e))

def getTimeOffsetSeconds(timeZoneOffset):
	if timeZoneOffset is None:
		return timeZoneOffset
	if isinstance(timeZoneOffset, int):
		return timeZoneOffset
	elif isinstance(timeZoneOffset, float):
		return timeZoneOffset
	elif isinstance(timeZoneOffset, str):
		pattern = re.compile(r"([+-])(\d{2})(\d{2})")
		match = pattern.match(timeZoneOffset)
		if match:
			sign = match.group(1)
			hours = int(match.group(2))
			minutes = int(match.group(3))
			total_offset_minutes = (hours * 60 + minutes) * (-1 if sign == '-' else 1)
			offset = datetime.timedelta(minutes=total_offset_minutes)
			return offset.total_seconds()
		else:
			raise errors.ParameterException("UnknownTimeZoneOffsetError:" + str(timeZoneOffset))
	else:
		raise errors.ParameterException("UnknownTimeZoneOffsetError:" + str(timeZoneOffset))

class UltipaDatetime:
	'''
	Processing class for date and time related operations.
	'''
	year = 0
	month = 0
	day = 0
	hour = 0
	minute = 0
	second = 0
	microsecond = 0

	@classmethod
	def datetimeStr2datetimeInt(self, strDatetime: datetime.datetime):
		'''
		Convert a datatime string into a customized datatime integer.

		Args:
			strDatetime:

		Returns:

		'''

		if isinstance(strDatetime, str):
			try:
				data = datetime.datetime.strptime(strDatetime, "%Y-%m-%d %H:%M:%S.%f%z")
			except:
				try:
					data = datetime.datetime.strptime(strDatetime, "%Y-%m-%d %H:%M:%S.%f")
				except ValueError as e:
					try:
						data = datetime.datetime.strptime(strDatetime, "%Y-%m-%d %H:%M:%S")
					except ValueError as e:
						try:
							data = datetime.datetime.strptime(strDatetime, "%Y-%m-%d")
						except ValueError as e:
							raise ParameterException(e)

		elif isinstance(strDatetime, datetime.datetime):
			data = strDatetime
		else:
			raise ParameterException('strDatetime must str %Y-%m-%d %H:%M:%S.%f or datetime type')
		self.year = data.year
		self.month = data.month
		self.day = data.day
		self.hour = data.hour
		self.minute = data.minute
		self.second = data.second
		self.microsecond = data.microsecond

		if self.year >= 70 and self.year < 100:
			self.year += 1900
		elif self.year < 70:
			self.year += 2000

		datetime_int = 0
		year_month = self.year * 13 + self.month
		datetime_int |= (year_month << 46)
		datetime_int |= (self.day << 41)
		datetime_int |= (self.hour << 36)
		datetime_int |= (self.minute << 30)
		datetime_int |= (self.second << 24)
		datetime_int |= self.microsecond
		return datetime_int

	@classmethod
	def timestampStr2timestampInt(self, strDatetime: str, timeZone, timeZoneOffset=0):
		'''
		Convert strings of datetime, timezone and timezone-offset into the Unix timestamp integer in seconds.

		Args:
			strDatetime:
			timeZone:
			timeZoneOffset:

		Returns:

		'''

		try:
			tzinfo = None
			dt = parse(strDatetime)
			if dt.utcoffset() is not None:
				offset_hours = int(dt.utcoffset().total_seconds() / 3600)
				tzinfo = UTC(offset_hours, timeZoneOffset)

			if timeZone is not None:
				total_seconds = getTimeZoneSeconds(timeZone)
				tzinfo = UTC(0, total_seconds)
			else:
				if timeZoneOffset is not None:
					total_seconds = getTimeOffsetSeconds(timeZoneOffset)
					tzinfo = UTC(0, total_seconds)

			timestamp = datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute,
										  second=dt.second, tzinfo=tzinfo)
			return int(timestamp.timestamp())
		except ValueError as e:
			raise ParameterException(e)

	@staticmethod
	def datetimeInt2datetimeStr(datetime_int):
		'''
		Convert the customized datetime integer into a datetime string

		Args:
			datetime_int:

		Returns:

		'''
		if datetime_int < 0:
			return ""
		from datetime import datetime
		year_month = ((datetime_int >> 46) & 0x1FFFF)
		year = year_month // 13
		month = year_month % 13
		day = ((datetime_int >> 41) & 0x1F)
		hour = ((datetime_int >> 36) & 0x1F)
		minute = ((datetime_int >> 30) & 0x3F)
		second = ((datetime_int >> 24) & 0x3F)
		microsecond = (datetime_int & 0xFFFFFF)

		def pixString(s, length):
			s = "000000" + str(s)
			return s[len(s) - length:]

		if year == 0:
			return f"{pixString(year, 4)}-{pixString(month, 2)}-{pixString(day, 2)} {pixString(hour, 2)}:{pixString(minute, 2)}:{pixString(second, 2)}.{pixString(microsecond, 2)}"
		if microsecond == 000000:
			ret = datetime(year, month, day, hour, minute, second)
			ret = ret.strftime("%Y-%m-%d %H:%M:%S")
		else:
			ret = datetime(year, month, day, hour, minute, second, microsecond)
			ret = ret.strftime("%Y-%m-%d %H:%M:%S.%f")
		return ret

	@staticmethod
	def timestampInt2timestampStr(datetime_int, timeZone: str = None, timeZoneOffset: int = 0):
		timeStamp = float(datetime_int)
		offset_hours = 0
		if timeZone:
			total_seconds = getTimeZoneSeconds(timeZone)
			offset_hours = int(total_seconds / 3600)
		if timeZoneOffset is None:
			timeZoneOffset = 0
		otherStyleTime = datetime.datetime.fromtimestamp(timeStamp, tz=UTC(offset_hours, timeZoneOffset))
		return str(otherStyleTime)


def wrapper(func):
	'''
	Measures the execution time of a method.

	Args:
		func:

	Returns:

	'''
	
	def inner(*args, **kwargs):
		start_time = time.time()
		res = func(*args, **kwargs)
		end_time = time.time()
		result = end_time - start_time
		print('func %s time is: %.3fs' % (func.__name__, result))
		return res

	return inner


class DateTimestamp(object):
	"""
	A class that realizes the mutual conversion of datetime and timestamp.

	"""

	def __init__(self, date=None):
		if date is None:
			self.timestamp = int(time.time())
			self.datetime = self._toDatetime(self.timestamp)
		else:
			### Judge whether the input date is a timestamp ###
			if isinstance(date, int):
				self.timestamp = date
				self.datetime = self._toDatetime(date)
			else:
				self.timestamp = self._toTimestamp(date)
				self.datetime = date

		if self.timestamp == False:
			self.year = self.month = self.day = self.hour = self.minute = self.second = False
		else:
			self._localtime = time.localtime(self.timestamp) # Parse the tuples from the timestamp
			self.year = self._localtime.tm_year  # Assign year tuple
			self.month = self._localtime.tm_mon  # Assign month tuple
			self.day = self._localtime.tm_mday  # Assign day tuple
			self.hour = self._localtime.tm_hour  # Assign hour tuple
			self.minute = self._localtime.tm_min  # Assign minute tuple
			self.second = self._localtime.tm_sec  # Assign second tuple

	def _toDatetime(self, timestamp):
		"""
		Convert timestamp to datetime

		"""
		try:
			timeStamp = float(timestamp)
			timeArray = time.localtime(timeStamp)
			return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		except:
			return False

	def _toTimestamp(self, datetimeString):
		"""
		Convert datetime to timestamp

		"""
		try:
			return int(time.mktime(time.strptime(datetimeString, "%Y-%m-%d %H:%M:%S")))
		except:
			return False

	def __str__(self):
		return self.datetime




def getTimeZoneOffset(requestConfig, defaultConfig):
	'''
	Get timezone offset

	Args:
		requestConfig:

		defaultConfig:

	Returns:

	'''

	timeZone = requestConfig.timeZone
	if timeZone is not None:
		return getTimeZoneSeconds(timeZone)
	timeZoneOffset = requestConfig.timeZoneOffset
	return getTimeOffsetSeconds(timeZoneOffset)
