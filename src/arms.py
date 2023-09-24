import os
import os.path
import pathlib

class Arms:
	def __init__(self, campaign_dir):
		self.base = '{campaign_dir}/Arms'.format(campaign_dir=campaign_dir)

	def __path(self, name):
		return '{base}/{name}.png'.format(base=self.base, name=name)

	def exists(self, name):
		path=self.__path(name)
		return os.path.isfile(path)

	def path(self, name):
		if not self.exists(name):
			return None
		return self.__path(name)

	def all_visible(self):
		files = os.listdir(self.base)
		files = [f.replace('.png', '') for f in files if os.path.isfile(self.base+'/'+f)]
		files.sort()
		return files


