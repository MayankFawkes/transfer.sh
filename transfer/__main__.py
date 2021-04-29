# -*- coding: utf-8 -*-
"""
main working functions file
"""

import requests, re
from time import time
from transfer.request import MakeRequest
from transfer.exceptions import FileTooLarge, PrepareError
from random import choices
from string import digits, ascii_uppercase, ascii_lowercase

class Upload(MakeRequest):
	'''Upload file

	:param str file: name of the file of full location
	:param **kwargs: Optional arguments that :class:`MakeRequest <MakeRequest>` class takes.
	'''
	def __init__(self, file:str, verbose:bool=False, force:bool=False, cli:bool=False,**kwargs):
		super().__init__(file=file, **kwargs)

		start = time()
		self.verbose = verbose
		if self.verbose:
			print("Preparing upload file...")

		if not force:
			try:
				self.prepare()
			except:
				raise PrepareError()

		response = self._send(**self.kwargs)

		assert response.status_code == 200, response.reason

		self.uploading_process_time = time() - start

		self._link = self.process(response)

		if cli:
			self._cli()

	def _send(self, **kwargs) -> requests.Response:
		'''make put request to upload file

		:return: :class:`requests.Response <requests.Response>` object
		:rtype: requests.Response
		'''
		return requests.put(**kwargs)

	def prepare(self):
		response = requests.get(self.url, headers={"accept": "text/html"})
		assert response.status_code == 200, response.reason

		pattern = re.compile(r"<h3>Upload up to ([0-9]+) (GB|MB)</h3>")

		size = {
			"MB": 1024*1024,
			"GB": 1024*1024*1024
		}
		nsize, type = re.findall(pattern, response.text)[0]

		self._max_file_limit = int(nsize)*size[type]

		if self._max_file_limit < self._len:
			raise FileTooLarge(self._max_file_limit)

	def _gen_hash(self) -> str:
		return "".join([
				*choices(ascii_uppercase+ascii_lowercase, k=2),
				*choices(digits, k=4),
				*choices(ascii_uppercase+ascii_lowercase, k=2)
				])


	def process(self, response:requests.Response) -> str:
		self.data = {
			"file": self._file_name,
			"hash": self._gen_hash(),
			"created on": response.headers.get("Date"),
			"delete url": response.headers.get("X-Url-Delete"),
			"url": response.text
		}
		return response.text

	def _cli(self) -> None:
		if self.verbose:
			print(
				f"Uploading time: {self.uploading_time:.2f}", 
				f"Server processing time: {(self.uploading_process_time - self.uploading_time):.2f}",
				sep=" | "
			)
		print(f"Link: {self._link}")
		if self.verbose:
			print(f"Hash: {self.data.get('hash')}")
			print(f"Delete: {self.data.get('delete url')}")
			print(f"Created on: {self.data.get('created on')}")

	@property
	def link(self):
		return self._link
	


class Remove:
	def __init__(self, *args, **kwargs):
		response = self._send(*args, **kwargs)
		if response.status_code == 200:
			self.status = True
			self.reason = "Successful delete" 
		elif response.status_code == 404:
			self.status = True
			self.reason = "Not found, already deleted"
		else:
			self.status = False
			self.reason = response.reason


	def _send(self, *args, **kwargs) -> requests.Response:
		'''make delete request to delete uploaded file

		:return: :class:`requests.Response <requests.Response>` object
		:rtype: requests.Response
		'''
		return requests.delete(*args, **kwargs)