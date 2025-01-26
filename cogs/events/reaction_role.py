import nextcord as nc
from nextcord.ext import commands
from utils import ReactionConfig

config = ReactionConfig()

class ReactionRoleEvent(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    async def get_role(reaction: nc.RawReactionActionEvent, member: nc.Member):
        message_reactions = config.get_message_reactions(str(reaction.message_id))

        if message_reactions:
            if str(reaction.emoji.name) in message_reactions:
                role_id = message_reactions[str(reaction.emoji.name)]
                print(member)
                return await member.guild.fetch_role(role_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: nc.RawReactionActionEvent):

        guild = await self.bot.fetch_guild(reaction.guild_id)
        member = await guild.fetch_member(reaction.user_id)
        
        role = await self.get_role(reaction, member)
        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction: nc.RawReactionActionEvent):
        
        guild = await self.bot.fetch_guild(reaction.guild_id)
        member = await guild.fetch_member(reaction.user_id)
        
        role = await self.get_role(reaction, member)
        if role:
            await member.remove_roles(role)


def setup(bot):
    bot.add_cog(ReactionRoleEvent(bot))
