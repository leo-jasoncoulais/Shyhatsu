
from json import load, dump

def get_value(key):

        with open("config.json", "r") as file:
            config = load(file)
            return config[key]

def set_value(key, value):

    config = {}

    with open("config.json", "r") as file:
        config = load(file)
        config[key] = value

    with open("config.json", "w") as file:

        dump(config, file, indent=4)
