
from json import load, dump

class Config:

    def __init__(self):
        self.file = "config.json"

    def get_config(self):
        with open(self.file, "r") as file:
            return load(file)

    def get_value(self, key):
        return self.get_config()[key]
        
    def set_value(self, key, value):
        config = self.get_config()
        with open(self.file, "w") as file:
            config[key] = value
            dump(config, file, indent=4)
