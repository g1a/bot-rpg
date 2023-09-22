import os
import os.path
import pathlib
import datetime
from datetime import datetime
from datetime import timedelta
from pytimeparse.timeparse import timeparse

from arms import Arms

class Campaign:
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.base = '{project}/Campaigns/{id}'.format(project=pathlib.Path(__file__).parent.resolve(), id=self.id)
		self.campaign_time = datetime.fromisoformat('1494-06-01 12:00:00')

	def arms(self):
		return Arms(self.base)

	def set_time(self, time: str):
		self.campaign_time = datetime.fromisoformat(time)

	def time(self):
		return self.campaign_time.strftime('%a %Y %b %d at %I:%M %p').replace(' 0', ' ')

	def pass_time(self, delta: str):
		self.campaign_time += timedelta(seconds=timeparse(delta))
