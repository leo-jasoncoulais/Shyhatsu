import nextcord as nc
from nextcord.ext import commands
from utils import AutoRoleConfig

config = AutoRoleConfig()

class DefaultRoleCommand(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @nc.slash_command(description="Ajouter un rôle qui sera ajouté à tous les membres à leur arrivée.")
    async def ajouter_role(self, interaction: nc.Interaction,
            role: nc.Role = nc.SlashOption(description="Le rôle à donner à l'arrivée.", required=True),
        ):
        
        if not (interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:
            
            if role.id not in config.get_auto_role():
                config.add_auto_role(role.id)

            await interaction.send(f"Le role sera attribué à l'arrivée des membres ! <:yay:1274376322847739935>", ephemeral=True)

    @nc.slash_command(description="Retirer un rôle qui ne sera plus ajouté à tous les membres à leur arrivée.")
    async def retirer_role(self, interaction: nc.Interaction,
            role: nc.Role = nc.SlashOption(description="Le rôle à ne plus donner à l'arrivée.", required=True),
        ):
        
        if not (interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:
            
            if role.id in config.get_auto_role():
                config.remove_auto_role(role.id)

            await interaction.send(f"Le role ne sera plus attribué à l'arrivée des membres ! <:yay:1274376322847739935>", ephemeral=True)

def setup(bot):
    bot.add_cog(DefaultRoleCommand(bot))
