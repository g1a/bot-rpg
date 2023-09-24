import os
import os.path
import pathlib
import datetime
from datetime import datetime
from datetime import timedelta
from pytimeparse.timeparse import timeparse

from src.arms import Arms
from src.participants import Participants
from src.role_in_campaign import RoleInCampaign

class Campaign:
	def __init__(self, id, name, creator):
		self.id = id
		self.creator = creator
		self.name = name
		self.campaign_dir = '{project}/Campaigns/{id}'.format(project=pathlib.Path(__file__).parent.resolve().parent.resolve(), id=self.id)
		self.campaign_time = datetime.fromisoformat('1494-06-01 12:00:00')
		self.participants = Participants(creator)

	def arms(self):
		# TEMPORARY: Let everyone see the Laensburg arms
		everyoneIsLaensburgForNow = '{project}/Campaigns/857097491131662346'.format(project=pathlib.Path(__file__).parent.resolve().parent.resolve())
		return Arms(everyoneIsLaensburgForNow)
		#return Arms(self.campaign_dir)

	def set_time(self, time: str):
		self.campaign_time = datetime.fromisoformat(time)

	def time(self):
		return self.campaign_time.strftime('%a %Y %b %d at %I:%M %p').replace(' 0', ' ')

	def pass_time(self, delta: str):
		self.campaign_time += timedelta(seconds=timeparse(delta))
