# -*- coding: utf-8 -*-
"""
Helper classes file
"""

from mimetypes import guess_type
from time import time
from os.path import getsize, split
from datetime import timedelta

from typing import Generator
from typing import Dict
from typing import Union

class MakeRequest:
	'''Construct arguments to make request.

	:param str file: name of the file of full location
	:param object callback: this will get execute when ``self._run_callback`` is ``True``, default is ``False``
	:param dict cb_kwargs: additional keyword arguments for backback 

	'''

	def __init__(self, 
			file:str, 
			url:str=None, 
			callback:object=None,
			no_process_bar:bool=True,
			cb_kwargs:dict=dict(end="\r")
		):
		self._len = getsize(file)
		self._content_type, encoding = guess_type(file)

		self._file = open(file, "rb")
		tail, self._file_name = split(file)

		self.url = url or "https://transfer.sh"
		self._upload_url = f"{self.url}/{self._file_name}" if self.url[-1] != "/" else f"{self.url}{self._file_name}"

		self._progress = 0
		self._progress_in_second = 0

		self._callback = callback or self._progress_bar
		self._run_callback = not no_process_bar
		self._cb_kwargs = cb_kwargs
		self._started = self._last_callback = time()
		self._uploading_time = None

	def __len__(self):
		return self._len

	def iter_content(self, chunk_size:int=8192) -> Generator[int, bytes, None]:
		''' Generator so data cant be in memory in case of large files.

		:param int chunk_size: chunk size 

    	:rtype: collections.Iterable
		'''
		while data:=self._file.read(chunk_size):
			self._cb_kwargs.update({
				'size'	: self._len,
				'progress': self._progress,
				'in_second': self._progress_in_second
			})

			if self._run_callback and (time() - self._last_callback) >= 1.0:
				self._callback(**self._cb_kwargs)
				self._last_callback = time()
				self._progress_in_second = 0

			self._progress+=len(data)
			self._progress_in_second+=len(data)
			yield data

		self._cb_kwargs.update({
			'size'	: self._len,
			'progress': self._len,
			'in_second': self._progress_in_second,
			'end': '\n'
		})
		if self._run_callback:
			self._callback(**self._cb_kwargs)

		self._finally()

	def _progress_bar(self, 
			size=None, 
			progress=None,
			in_second=None, 
			loading_sign:str="█", 
			width:int=50, 
			end="\r"
		) -> None:
		percentage = (progress*width) // size
		print(f"Upload: |{loading_sign * percentage:{'-'}<{width}}| {percentage*(100//width):>3}%",
			f"{str(round(in_second/(1024*1024), 2))+'MB/s' if len(str(in_second//1024)) >= 4 else str(in_second//1024)+'Kb/s':>4}",
			f"EST: {self._est(size, progress, in_second):<15}",
			end=end, sep=' | ')

	def _est(self, size, progress, in_second) -> str:
		progress = progress or 1
		in_second = in_second or 1
		time = size//in_second - progress//in_second
		return str(timedelta(seconds=time))

	def _finally(self) -> None:
		self._uploading_time = time() - self._started

	@property
	def kwargs(self) -> Dict[str, Union[str, Generator[int, bytes, None], Dict[str, str]]]:
		return {
			"url": self._upload_url,
			"headers": self.headers,
			"data": self.iter_content()
		}
	
	@property
	def headers(self) -> Dict[str, str]:
		return {
			"Content-Type": self._content_type
		}

	@property
	def uploading_time(self) -> float:
		return self._uploading_time