import nextcord as nc
from nextcord.ext import commands
from os import listdir, getenv
from dotenv import load_dotenv

class Bot:

    def __init__(self):
        
        load_dotenv()
        self.bot = commands.Bot(intents=nc.Intents.all())
        self.load_cogs()

        self.run()
    
    def load_cogs(self):

        cogs = []

        for C in listdir("cogs/commands"):
            if C.endswith(".py"):
                cogs.append("cogs.commands."+C[:-3])

        for C in listdir("cogs/events"):
            if C.endswith(".py"):
                cogs.append("cogs.events."+C[:-3])

        self.bot.load_extensions(cogs)

    def run(self):
        
        self.bot.run(getenv("TOKEN"))

Bot()
