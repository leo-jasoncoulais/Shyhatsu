import nextcord as nc
from nextcord.ext import commands
from nextcord.ui import Button, View
from json import load, dump
from time import sleep

class ManageTicketCommand(commands.Cog):

    all_members = []

    def __init__(self, bot, config) -> None:
        self.bot = bot
        
        for c in config:
            self.__setattr__(c, config[c])

        ManageTicketCommand.all_members = bot.get_all_members()

    def update_config_file(self):

        config = {}

        with open("config.json", "r") as file:
            config = load(file)
            for c in config:
                config[c] = self.__getattribute__(c)

        with open("config.json", "w") as file:

            dump(config, file, indent=4)

    @nc.slash_command(description="Accepter un membre sur le serveur.")
    async def accepter_membre(self, interaction: nc.Interaction, membre:nc.Member = nc.SlashOption(choices=all_members)):

        guild = await self.bot.fetch_guild(self.GUILD_ID)
        await guild.fetch_roles()

        if not (interaction.user.top_role.permissions.manage_roles or interaction.user.top_role.permissions.administrator or interaction.user.id == guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        elif interaction.channel.category.id != self.TICKET_CATEGORY_ID:
            await interaction.send("Désolé, tu n'as pas le droit de faire cette commande ici... <:tristefrog:1274343966623400017>")

        else:
            role = guild.get_role(self.MEMBER_ROLE_ID)

            try:
                await membre.add_roles(role)
            except:
                pass

            await interaction.send(f"<@{membre.id}>, on te souhaite la bienvenue sur le serveur ! <:yay:1274376322847739935>\n-# Ce ticket sera supprimé dans 5 secondes ^^")

            sleep(5)

            await interaction.channel.delete()

    @nc.slash_command(description="Mettre en place le système de tickets.")
    async def configurer_tickets(self, 
            interaction: nc.Interaction,
            ticket_category: str = nc.SlashOption(description="La catégorie où les tickets seront créés.", required=True)
        ):

        async def allow_ticket_creation(interaction: nc.Interaction):
            
            if interaction.data["custom_id"] == "delete_ticket":

                self.TICKET_CHANNEL_ID = interaction.channel.id
                self.TICKET_CATEGORY_ID = int(ticket_category)

                self.update_config_file()

                await interaction.message.edit("Le système de tickets a été superbement configuré ! <:yay:1274376322847739935>", view=None)

                view = View()
                view.add_item(Button(style=nc.ButtonStyle.primary, label="Créer un ticket", custom_id="create_ticket"))
                
                embed = nc.Embed(
                    title="Ticket d'entrée <:petitefrog:1216663533928845322>",
                    description="Pour rentrer sur le serveur, merci d'ouvrir un ticket et répondre aux questions ! <:yay:1274376322847739935>",
                    color=nc.Color.green()
                )

                await interaction.channel.send(embed=embed, view=view)
                
                sleep(3)

                await interaction.message.delete()

            else:

                await interaction.message.edit("On fera la configuration plus tard. <:miamchoco:1216663553722023966>", view=None)

                sleep(3)

                await interaction.message.delete()

        guild = await self.bot.fetch_guild(self.GUILD_ID)
        await guild.fetch_roles()

        if not (interaction.user.top_role.permissions.manage_channels or interaction.user.top_role.permissions.administrator or interaction.user.id == guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:

            if self.TICKET_CHANNEL_ID:

                view = View()
                view.add_item(Button(style=nc.ButtonStyle.danger, label="Supprimer l'ancien système de tickets", custom_id="delete_ticket"))
                view.add_item(Button(style=nc.ButtonStyle.primary, label="Annuler", custom_id="cancel"))

                view.interaction_check = allow_ticket_creation

                await interaction.send("Il y a déjà un système de tickets, tu veux vraiment le supprimer pour en créer un nouveau ? <:OHHHH:1287740128806309930>", view=view)

            else:

                self.TICKET_CHANNEL_ID = interaction.channel.id
                self.TICKET_CATEGORY_ID = int(ticket_category)

                self.update_config_file()

                await interaction.send("Le système de tickets a été superbement configuré ! <:yay:1274376322847739935>", view=None)

                sleep(3)    

                await interaction.message.delete()

def setup(bot):
    with open("config.json", "r") as file:
        config = load(file)
        bot.add_cog(ManageTicketCommand(bot, config))
