import nextcord as nc
from nextcord.ext import commands

class ManageTicket(commands.Cog):

    all_members = []

    def __init__(self, bot) -> None:
        self.bot = bot
        self.GUILD_ID = 1108133087168172113
        self.MEMBER_ROLE_ID = 1108150462147989514
        ManageTicket.all_members = bot.get_all_members()

    @nc.slash_command(description="Accepter un membre sur le serveur.")
    async def accepter_membre(self, interaction: nc.Interaction, membre:nc.Member = nc.SlashOption(choices=all_members)):

        guild = await self.bot.fetch_guild(self.GUILD_ID)
        await guild.fetch_roles()

        if not (interaction.user.top_role.permissions.manage_roles or interaction.user.top_role.permissions.administrator):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        elif not interaction.channel.name.startswith("ticket"):
            await interaction.send("Désolé, tu n'as pas le droit de faire cette commande ici... <:tristefrog:1274343966623400017>")

        else:
            role = guild.get_role(self.MEMBER_ROLE_ID)

            try:
                await membre.add_roles(role)
            except:
                pass

            await interaction.send(f"<@{membre.id}>, on te souhaite la bienvenue sur le serveur ! <:yay:1274376322847739935>")

def setup(bot):
    bot.add_cog(ManageTicket(bot))
