import nextcord as nc
from nextcord.ext import commands
from json import load, dump

class ManageTicketEvent(commands.Cog):

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

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nc.SlashOption):
        
        if interaction.type == nc.InteractionType.component:

            if interaction.data["custom_id"] == "create_ticket":

                category: nc.CategoryChannel = await interaction.guild.fetch_channel(self.get_value("TICKET_CATEGORY_ID"))

                id = sum([int(i) for i in str(interaction.user.id)])

                channel = await category.create_text_channel(name=f"ticket-{id}", topic=str(interaction.user.id), overwrites={

                    interaction.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                    interaction.guild.get_role(self.get_value("STAFF_ROLE_ID")): nc.PermissionOverwrite(read_messages=True),
                    interaction.user: nc.PermissionOverwrite(read_messages=True)
                })

                embed = nc.Embed(title="Bienvenue à 𝐿'𝛼𝜋𝜏𝜄𝑞𝜇𝜀 ! ☕", description=f"Merci de répondre aux questions suivantes afin de valider ton arrivée sur le serveur! Un membre du staff te répondra dès que possible. 🐸\n\n🍉 Quel âge as-tu ?\n🍉 Que cherches-tu sur ce serveur?", color=nc.Color.green())
                
                await interaction.send("Le ticket a été créé ! <:yay:1274376322847739935>", ephemeral=True)

                await channel.send(embed=embed)
                msg = await channel.send(f"<@{interaction.user.id}><@&{self.get_value('STAFF_ROLE_ID')}>")
                await msg.delete()


def setup(bot):
    bot.add_cog(ManageTicketEvent(bot))
