import nextcord as nc
from nextcord.ext import commands
from os import listdir

bot = commands.Bot(intents=nc.Intents.all())

@bot.event
async def on_ready():
    print("Bot is connected.")

cogs = []

for C in listdir("cogs"):
    if C.endswith(".py"):
        cogs.append("cogs."+C[:-3])

bot.load_extensions(cogs)

bot.run("MTI4NzQ0MzYzNzA0Njg3MDAxNg.G8OxkW.Oxy9V2aOx0-nun2pHL3ZdwsSQyKC1I0oBVxgWo")
