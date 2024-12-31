import nextcord as nc
from nextcord.ext import commands
from json import load, dump

class ManageTicketEvent(commands.Cog):

    all_members = []

    def __init__(self, bot, config) -> None:
        self.bot = bot
        
        for c in config:
            self.__setattr__(c, config[c])

        ManageTicketEvent.all_members = bot.get_all_members()

    def update_config_file(self):

        config = {}

        with open("config.json", "r") as file:
            config = load(file)
            for c in config:
                config[c] = self.__getattribute__(c)

        with open("config.json", "w") as file:

            dump(config, file, indent=4)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nc.SlashOption):
        
        if interaction.type == nc.InteractionType.component:

            if interaction.data["custom_id"] == "create_ticket":

                guild: nc.Guild = await self.bot.fetch_guild(self.GUILD_ID)
                category: nc.CategoryChannel = await guild.fetch_channel(self.TICKET_CATEGORY_ID)

                id = sum([int(i) for i in str(interaction.user.id)])

                channel = await category.create_text_channel(name=f"ticket-{id}", overwrites={
                    guild.default_role: nc.PermissionOverwrite(read_messages=False),
                    guild.get_role(self.STAFF_ROLE_ID): nc.PermissionOverwrite(read_messages=True),
                    interaction.user: nc.PermissionOverwrite(read_messages=True)
                })

                embed = nc.Embed(title="Bienvenue à 𝐿'𝛼𝜋𝜏𝜄𝑞𝜇𝜀 ! ☕", description=f"Merci de répondre aux questions suivantes afin de valider ton arrivée sur le serveur! Un membre du staff te répondra dès que possible. 🐸\n\n🍉 Quel âge as-tu ?\n🍉 Que cherches-tu sur ce serveur?", color=nc.Color.green())
                
                await interaction.send("Le ticket a été créé ! <:yay:1274376322847739935>", ephemeral=True)

                await channel.send(embed=embed)
                msg = await channel.send(f"<@{interaction.user.id}><@&{self.STAFF_ROLE_ID}>")
                await msg.delete()


def setup(bot):
    with open("config.json", "r") as file:
        config = load(file)
        bot.add_cog(ManageTicketEvent(bot, config))
