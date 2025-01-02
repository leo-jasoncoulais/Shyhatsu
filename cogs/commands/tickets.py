import nextcord as nc
from nextcord.ext import commands
from nextcord.ui import Button, View
from json import load, dump
from time import sleep

class ManageTicketCommand(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    def get_value(self, key):

        with open("config.json", "r") as file:
            config = load(file)
            return config[key]

    def write_value(self, key, value):

        config = {}

        with open("config.json", "r") as file:
            config = load(file)
            config[key] = value

        with open("config.json", "w") as file:

            dump(config, file, indent=4)

    @nc.slash_command(description="Accepter un membre sur le serveur.")
    async def accepter_membre(self, interaction: nc.Interaction):

        await interaction.guild.fetch_roles()

        if not (interaction.user.top_role.permissions.manage_roles or interaction.user.top_role.permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        elif interaction.channel.category.id != self.get_value("TICKET_CATEGORY_ID"):
            await interaction.send("Désolé, tu n'as pas le droit de faire cette commande ici... <:tristefrog:1274343966623400017>")

        else:

            role = interaction.guild.get_role(self.get_value("MEMBER_ROLE_ID"))
            
            member = interaction.guild.get_member(int(interaction.channel.topic))

            try:
                await member.add_roles(role)
            except:
                pass

            await interaction.send(f"<@{member.id}>, on te souhaite la bienvenue sur le serveur ! <:yay:1274376322847739935>\n-# Ce ticket sera supprimé dans 5 secondes ^^")

            sleep(5)

            await interaction.channel.delete()
    
    @nc.slash_command(description="Refuser un membre sur le serveur.")
    async def refuser_membre(self, interaction: nc.Interaction):

        await interaction.guild.fetch_roles()

        if not (interaction.user.top_role.permissions.manage_roles or interaction.user.top_role.permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        elif interaction.channel.category.id != self.get_value("TICKET_CATEGORY_ID"):
            await interaction.send("Désolé, tu n'as pas le droit de faire cette commande ici... <:tristefrog:1274343966623400017>")

        else:
            member = interaction.guild.get_member(int(interaction.channel.topic))

            await interaction.send(f"Désolé <@{member.id}>, tu ne réponds pas aux exigences du serveur... <:tristefrog:1274343966623400017>\n-# Ce ticket sera supprimé dans 5 secondes ^^")

            try:
                await member.send("Désolé, tu ne réponds pas aux exigences du serveur... Tu as donc été expulsé.\n-# Si tu n'avais pas l'âge requis, revient quand tu l'auras ^^")
            except:
                pass

            await member.kick()

            sleep(5)

            await interaction.channel.delete()

    @nc.slash_command(description="Mettre en place le système de tickets.")
    async def configurer_tickets(self, 
            interaction: nc.Interaction,
            ticket_category: nc.CategoryChannel = nc.SlashOption(description="La catégorie où les tickets seront créés.", required=True)
        ):

        async def allow_ticket_creation(interaction: nc.Interaction):
            
            if interaction.data["custom_id"] == "delete_ticket":

                self.write_value("TICKET_CHANNEL_ID", interaction.channel.id)
                self.write_value("TICKET_CATEGORY_ID", ticket_category.id)

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

        await interaction.guild.fetch_roles()

        if not (interaction.user.top_role.permissions.manage_channels or interaction.user.top_role.permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:

            if self.get_value("TICKET_CHANNEL_ID"):

                view = View()
                view.add_item(Button(style=nc.ButtonStyle.danger, label="Supprimer l'ancien système de tickets", custom_id="delete_ticket"))
                view.add_item(Button(style=nc.ButtonStyle.primary, label="Annuler", custom_id="cancel"))

                view.interaction_check = allow_ticket_creation

                await interaction.send("Il y a déjà un système de tickets, tu veux vraiment le supprimer pour en créer un nouveau ? <:OHHHH:1287740128806309930>", view=view)

            else:

                self.write_value("TICKET_CHANNEL_ID", interaction.channel.id)
                self.write_value("TICKET_CATEGORY_ID", ticket_category.id)

                await interaction.send("Le système de tickets a été superbement configuré ! <:yay:1274376322847739935>")

                view = View()
                view.add_item(Button(style=nc.ButtonStyle.primary, label="Créer un ticket", custom_id="create_ticket"))
                
                embed = nc.Embed(
                    title="Ticket d'entrée <:petitefrog:1216663533928845322>",
                    description="Pour rentrer sur le serveur, merci d'ouvrir un ticket et répondre aux questions ! <:yay:1274376322847739935>",
                    color=nc.Color.green()
                )

                await interaction.channel.send(embed=embed, view=view)

                sleep(3)    

                await interaction.delete_original_message()

def setup(bot):
    bot.add_cog(ManageTicketCommand(bot))
