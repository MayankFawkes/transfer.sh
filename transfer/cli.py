# -*- coding: utf-8 -*-
"""
Cli file
"""
import sys

if __name__ == '__main__':
	sys.path.insert(0,'..')


from transfer import Upload, Remove, __version__, __github__
from transfer.table import Table
import argparse, re, signal
from os import access, R_OK
from os.path import isfile, sep
from typing import Dict
from typing import Union
from typing import List
from json import loads, dumps
from tempfile import gettempdir


class ActionCheck(object):
	AVAIABLE_TEST = ["file", "hash"]
	def __init__(self, test:str):
		self.test = test
		assert test in self.AVAIABLE_TEST, "Invalid Test"
		self._hash_pattern = re.compile(r"([a-zA-Z]){2}([0-9]){4}([a-zA-Z]){2}")

	def match_hash(self, value:str) -> bool:
		if re.match(self._hash_pattern, value):
			return True
		return False

	def file(self, value:str) -> Dict[str, str]:
		if isfile(value) and access(value, R_OK):
			return dict(type="file", value=value)
		raise argparse.ArgumentTypeError(f"can't open '{value}' No such file or do not have permissions")

	def hash(self, value:str) -> Dict[str, str]:
		if self.match_hash(value) and len(value) == 8:
			return dict(type="hash", value=value)
		raise argparse.ArgumentTypeError(f"Invalid hash")

	def __call__(self, value):
		return getattr(self, self.test)(value)

class log:
	def __init__(self):
		self.FILE_NAME = self._get_file_name()
		if not isfile(self.FILE_NAME):
			open(self.FILE_NAME, 'a').close()

	def _get_file_name(self, name:str=".transfer.log"):
		return f"{gettempdir()}{sep}{name}"

	def _get(self) -> Union[List[None], List[Dict[str, str]]]:
		with open(self.FILE_NAME, "r") as file:
			data = file.read()
		file.close()
		if data:
			return loads(data)
		return list()

	def _save(self, data:List[Dict[str, str]]=list()) -> None:
		with open(self.FILE_NAME, "w") as file:
			file.write(dumps(data))
		file.close()

	def _filter(self, data:List[Dict[str, str]], hash:str) -> Union[Dict[str, str], None]:
		for log in data:
			if log.get("hash") == hash:
				return log
		raise KeyError(f"Hash not found")

	def _add_log(self, data:Dict[str, str]):
		log = self._get()
		log.append(data)
		self._save(log)

	def _remove_log_with_hash(self, log:Dict[str, str]):
		logs = self._get()
		logs.remove(log)
		self._save(logs)


class CLI(log):
	def __init__(self):
		signal.signal(signal.SIGINT, self.bye)
		signal.signal(signal.SIGTERM, self.bye)

		super().__init__()

		args = self.get_args()

		if args.type.get("type") == "file":
			self._upload(args)

		elif args.type.get("type") == "list":
			self._list()

		elif args.type.get("type") == "hash":
			self._remove(args)

	def _upload(self, namespace:argparse.Namespace) -> None:
		namespace = vars(namespace)
		namespace.__setitem__("file", namespace.pop("type").get("value"))
		res = Upload(cli=True,**namespace)
		self._add_log(res.data)

	def _remove(self, namespace:argparse.Namespace):
		try:
			namespace = vars(namespace)
			namespace.__setitem__("hash", namespace.pop("type").get("value"))

			logs = self._get()

			log = self._filter(**namespace, data=logs)

			response = Remove(url=log.get("delete url"))

			if response.status:
				self._remove_log_with_hash(log)
				print(f"Deleted: {response.reason}")

			else:
				print(f"Error: {response.reason}")


		except KeyError:
			print(f"Error: Invalid hash, Not found.")

	def _list(self):
		logs = self._get()

		table = Table(["file", "hash", "created", "url"], margin=5)

		for log in logs:
			table.add_table(log.get("file"), log.get("hash"), log.get("created on"), log.get("url"))

		table.display()



	def get_args(self) -> argparse.Namespace:
		parser = argparse.ArgumentParser(description="transfer.sh CLI")

		parser.add_argument("-V", "--version", action="version", version=f"transfer.sh version {__version__} ({__github__})")
		sub_parser = parser.add_subparsers(
							help="Help", 
							metavar="Options", 
							required=True,
							title="Required Options"
							)

		c1 = sub_parser.add_parser("remove", aliases=["rm"], help="Remove uploaded file.")
		c1.add_argument("type", type=ActionCheck("hash"), help="Hash of already uploaded file.")

		c2 = sub_parser.add_parser("upload", aliases=["up"], help="Upload file.")
		c2.add_argument("type", type=ActionCheck("file"), help="File you want to upload.")

		c2.add_argument("-v", "--verbose", required=False, action="store_true", help="Enable Verbose mode for extra logs.")
		c2.add_argument("-np", "--no-process-bar", required=False, action="store_true", help="Disable process bar.")
		c2.add_argument("-s", "--url", required=False, help="Third-party transfer.sh servers.")
		
		c3 = sub_parser.add_parser("list", aliases=["l"], help="List all uploaded files.")
		c3.add_argument("-s", "--show", action="store_const", required=True, const=dict(type="list"), dest="type")
		return parser.parse_args()

	def bye(self, signum, frame):
		print("Quiting...")
		sys.exit(0)



def main():
	CLI()

if __name__ == "__main__":
	main()
