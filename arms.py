import os
import os.path
import pathlib

class Arms:
	def __init__(self, base):
		self.base = base

	def _path(self, name):
		return '{base}/Arms/{name}.png'.format(base=self.base, name=name)

	def exists(self, name):
		path=self._path(name)
		return os.path.isfile(path)

	def path(self, name):
		if not self.exists(name):
			return None
		return self._path(name)

