# -*- coding: utf-8 -*-
"""
Exceptions classes
"""


class TransferError(Exception):
	def __init__(self, msg):
		self.msg = msg
		Exception.__init__(self, msg)

	def __str__(self):
		return self.msg

	__repr__ = __str__


class FileTooLarge(TransferError):
	def __init__(self, limit: int):
		"""
		:param int limit:
			Max uploading size.
		"""
		self._limit = limit
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return f'Max file size limit is {self.limit}'

	@property
	def limit(self):
		return str(round(self._limit/(1024*1024*1024), 2))+'GB' if len(str(self._limit//(1024*1024))) >= 4 else str(round(self._limit/(1024*1024), 2))+'MB'

class PrepareError(TransferError):
	def __init__(self):
		"""
		:param int limit:
			Max uploading size.
		"""
		super().__init__(self.error_message)

	@property
	def error_message(self):
		return f'Unable to fetch prepare data from site try --force.'