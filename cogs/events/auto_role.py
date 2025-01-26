import nextcord as nc
from nextcord.ext import commands
from utils import AutoRoleConfig

config = AutoRoleConfig()

class AutoRoleEvent(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nc.Member):

        for role_id in config.get_default_role():
            role = await member.guild.fetch_role(role_id)
            await member.add_roles(role)



def setup(bot):
    bot.add_cog(AutoRoleEvent(bot))
