import nextcord as nc
from nextcord.ext import commands
from utils import TicketConfig

config = TicketConfig()

class SetupCommand(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nc.slash_command(description="Configurer rôles.")
    async def setup(self, interaction: nc.Interaction,
            membre: nc.Role = nc.SlashOption(description="Le rôle membre.", required=True),
            staff: nc.Role = nc.SlashOption(description="Le rôle staff.", required=True),
        ):

        if not (interaction.user.top_role.permissions.manage_roles or interaction.user.top_role.permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:
            config.set_member_role(membre.id)
            config.set_staff_role(staff.id)

            await interaction.send(f"Les rôles sont configurés ! <:yay:1274376322847739935>", ephemeral=True)

def setup(bot):
    bot.add_cog(SetupCommand(bot))
