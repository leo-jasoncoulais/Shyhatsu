import nextcord as nc
from nextcord.ext import commands
from json import load, dump

class SetupCommand(commands.Cog):

    def __init__(self, bot, config) -> None:
        self.bot = bot
        
        for c in config:
            self.__setattr__(c, config[c])


    def update_config_file(self):

        config = {}

        with open("config.json", "r") as file:
            config = load(file)
            for c in config:
                config[c] = self.__getattribute__(c)

        with open("config.json", "w") as file:

            dump(config, file, indent=4)

    @nc.slash_command(description="Configurer rôles.")
    async def setup(self, interaction: nc.Interaction,
            membre: nc.Role = nc.SlashOption(description="Le rôle membre.", required=True),
            staff: nc.Role = nc.SlashOption(description="Le rôle staff.", required=True),
        ):

        if not (interaction.user.top_role.permissions.manage_roles or interaction.user.top_role.permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:
            self.MEMBER_ROLE_ID = membre.id
            self.STAFF_ROLE_ID = staff.id
            
            self.update_config_file()

            await interaction.send(f"Les rôles sont configurés ! <:yay:1274376322847739935>")

def setup(bot):
    with open("config.json", "r") as file:
        config = load(file)
        bot.add_cog(SetupCommand(bot, config))
