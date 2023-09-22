import os
import os.path
import pathlib

from arms import Arms

class Campaign:
	def __init__(self, id):
		self.id = id
		self.base = '{project}/Campaigns/{id}'.format(project=pathlib.Path(__file__).parent.resolve(), id=self.id)

	def arms(self):
		return Arms(self.base)

