from enum import IntEnum

class RoleInCampaign(IntEnum):
    VISITOR = 1
    PLAYER = 2
    GAME_MASTER = 3
    CREATOR = 4

    @classmethod
    def all_roles(cls):
    	return [str(r.name) for r in RoleInCampaign]

    @classmethod
    def value_of(cls, value):
        for k, v in cls.__members__.items():
            if k == value:
                return v
        else:
            return RoleInCampaign.VISITOR
