import nextcord as nc
from nextcord.ext import commands
from utils import ReactionConfig

config = ReactionConfig()

class ReactionRoleCommand(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nc.slash_command(description="Ajouter une réaction à un message pour obtenir un rôle.")
    async def ajouter_reaction(self, interaction: nc.Interaction,
            message_id: str = nc.SlashOption(description="L'ID du message contenant la réaction.", required=True),
            emoji: str = nc.SlashOption(description="L'emoji à ajouter.", required=True),
            role: nc.Role = nc.SlashOption(description="Le rôle à donner en cas d'interaction.", required=True),
        ):
        
        if not (interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.administrator or interaction.user.id == interaction.guild.owner_id):
            await interaction.send("Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>")

        else:
            
            try:
                message = await interaction.channel.fetch_message(int(message_id))
            except:
                await interaction.send("Le message n'a pas été trouvé... <:tristefrog:1274343966623400017>")
                return
            
            try:
                emoji = nc.PartialEmoji(name=emoji)
                await message.add_reaction(emoji)
            except:
                await interaction.send("L'emoji n'a pas été trouvé... <:tristefrog:1274343966623400017>")
                return
            
            reactions = config.get_message_reactions(message_id)
            
            if reactions is None:
                reactions = {}

            reactions[emoji.name] = role.id

            config.set_message_reactions(message_id, reactions)

            await interaction.send(f"La réaction a été ajoutée ! <:yay:1274376322847739935>", ephemeral=True)

def setup(bot):
    bot.add_cog(ReactionRoleCommand(bot))
