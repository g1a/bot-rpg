import os
import os.path
import pathlib

from src.role_in_campaign import RoleInCampaign

class Participants:
	def __init__(self, creator):
		self.creator = creator
		self.users = {creator: RoleInCampaign.CREATOR}
		self.masquerade = {}

	def add(self, user_id: str, role: RoleInCampaign = RoleInCampaign.PLAYER):
		self.users[user_id] = role

	def actual_role(self, user_id):
		return self.users.get(user_id, RoleInCampaign.VISITOR)

	def effective_role(self, user_id):
		return self.masquerade.get(user_id, self.actual_role(user_id))

	def act_as(self, user_id, role: RoleInCampaign):
		if not user_id in self.users:
			return False
		if role.value > self.actual_role(user_id).value:
			return False
		self.masquerade[user_id] = role
		return True

	def authorized(self, user_id: str, required_role: RoleInCampaign = RoleInCampaign.GAME_MASTER):
		return self.effective_role(user_id).value >= required_role.value
