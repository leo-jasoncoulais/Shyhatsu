from copy import copy
from json import load, dump

class Config:

    def __init__(self):
        self.file = "config.json"

    def get_config(self):
        with open(self.file, "r") as file:
            return load(file)
        
    def set_config(self, config):
        with open(self.file, "w") as file:
            dump(config, file, indent=4)

    def get_value(self, key):
        return self.get_config()[key]
        
    def set_value(self, key, value):
        config = self.get_config()
        with open(self.file, "w") as file:
            config[key] = value
            dump(config, file, indent=4)

class TicketConfig:

    def __init__(self):

        self.config = Config()
        self.name = "TICKETS"

        self.help_channel = "HELP_CHANNEL_ID"
        self.admission_channel = "ADMISSION_CHANNEL_ID"

        self.help_category = "HELP_CATEGORY_ID"
        self.admission_category = "ADMISSION_CATEGORY_ID"

        self.general_chat = "GENERAL_CHANNEL_ID"

        self.staff_role = "STAFF_ROLE_ID"
        self.member_role = "MEMBER_ROLE_ID"

        attributes = self.__dict__.copy()

        for attr in attributes:

            if attr == "name" or attr == "config":
                continue

            key = self.__getattribute__(attr)

            get_function = lambda key=key: self.get_value(key)
            self.__setattr__(f"get_{attr}", get_function)

            set_function = lambda value, key=key: self.set_value(key, value)
            self.__setattr__(f"set_{attr}", set_function)

    def get_value(self, key):
        return self.config.get_value(self.name)[key]

    def set_value(self, key, value):
        config = self.config.get_config()
        with open(self.config.file, "w") as file:
            config[self.name][key] = value
            dump(config, file, indent=4)

class ReactionConfig:

    def __init__(self):
        
        self.config = Config()
        self.name = "REACTION_ROLE"

    def get_message_reactions(self, message_id: str):
        config = self.config.get_value(self.name)
        if message_id in config:
            return config[message_id]
        
    def set_message_reactions(self, message_id: str, reactions: dict):
        config = self.config.get_config()
        with open(self.config.file, "w") as file:
            config[self.name][message_id] = reactions
            dump(config, file, indent=4)

class AutoRoleConfig:

    def __init__(self):
        
        self.config = Config()
        self.name = "AUTO_ROLE"

    def get_default_role(self):
        return self.config.get_value(self.name)
    
    def add_auto_role(self, role_id: int):
        config = self.config.get_config()
        with open(self.config.file, "w") as file:
            config[self.name].append(role_id)
            dump(config, file, indent=4)

    def remove_auto_role(self, role_id: int):
        config = self.config.get_config()
        with open(self.config.file, "w") as file:
            config[self.name].remove(role_id)
            dump(config, file, indent=4)
