import nextcord as nc
from nextcord.ext import commands


class EclipseCommand(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nc.slash_command(description="Permet d'eclipser un utilisateur")
    async def eclipse(self, interaction: nc.Interaction, member: nc.Member = nc.SlashOption(description="Membre à éclipser", required=True)):
        
        if not (interaction.user.top_role.permissions.ban_members or interaction.user.top_role.permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:
            await member.ban(reason="Tu l'as cherché.")
            await interaction.send(f"{member.mention} a été éclipsé ! <:yay:1274376322847739935>", ephemeral=True)


def setup(bot):
    bot.add_cog(EclipseCommand(bot))
