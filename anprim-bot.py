import nextcord
from nextcord.ext import (commands,application_checks,tasks)
import time

async def get_webhook(channel: nextcord.TextChannel) -> nextcord.Webhook:
    if channel.type.value not in [0,2,5,13]:
        return None
    
    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.user==bot.user:
            return wh
    else:
        wh = await channel.create_webhook(name=bot.user.name)
        return wh

class MyDict():
    def __init__(self,default=None) -> None:
        self.default = default
        self.data = {}
    
    def __getitem__(self, item):
        if item not in self.data:
            return self.default
        return self.data[item]
    
    def __setitem__(self, key, value):
        self.data[key] = value


timeout = MyDict(0)

token = "MTE2Mzc0NzQxOTg2ODExOTA0MA.GA6nMN.oGDmsgTtQX-40ov51airPeziHflOg7Z2_XNSt0"
bot = commands.Bot(command_prefix='a.',intents=nextcord.Intents.all())

class IdeaModal(nextcord.ui.Modal):
    def __init__(self,channel: nextcord.TextChannel):
        super().__init__(
            "Предложить идею",
            timeout=5 * 60,  # 5 minutes
        )
        self.channel = channel

        self.idea = nextcord.ui.TextInput(
            label="Расскажи нам о своей идее",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Опиши свою идею как можно более подробно с примерами использования.",
            min_length=10,
            max_length=1800,
        )
        self.add_item(self.idea)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        name = interaction.user.display_name#interaction.user.global_name if interaction.user.global_name and interaction.user.name == interaction.user.display_name else interaction.user.display_name
        await interaction.response.defer(ephemeral=True)
        idea = self.idea.value
        embed = nextcord.Embed(
            title='Новая идея!',
            description='Будет идея или нет, зависит от вас!',
            color=0xffba08
        )
        embed.set_footer(
            text=name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name='Идея:',value=idea)
        mes = await self.channel.send(embed=embed)
        await mes.add_reaction("<a:tickmark:1170029771040759969>")
        await mes.add_reaction("<a:cross:1170029921314279544>")
        await mes.create_thread(name=f"Обсуждение идеи от {name}")
        timeout[interaction.user.id] = time.time()+1800

class PersistentView(nextcord.ui.View):
    def __init__(self,bot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Предложить идею", style=nextcord.ButtonStyle.green, custom_id="persistent_view:sug"
    )
    async def suggest(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if timeout[interaction.user.id] > time.time():
            await interaction.response.send_message(content=(
                    "Предложить идею можно только раз в 30 минут\n"
                    f"Следующия возможность подать идею будет через: <t:{timeout[interaction.user.id]:.0f}:R>"
                ),
                ephemeral=True
            )
            return
        channel = self.bot.get_channel(1170031835728859208)
        await interaction.response.send_modal(modal=IdeaModal(channel))



@bot.event
async def on_ready():
    bot.add_view(PersistentView(bot))
    bot.persistent_views_added = True
    print(f"The bot is registered as {bot.user}")


@bot.command()
@commands.has_any_role(1169257391058079814,1163742629289271316)
async def button_suggest(ctx:commands.Context):
    await ctx.message.delete()
    await ctx.send('Предложи свою идею для проекта!',view=PersistentView(bot))

@bot.command()
@commands.is_owner()
async def shutdown(ctx:commands.Context):
    await bot.close()


if __name__ == "__main__":
    bot.persistent_views_added = False
    bot.run(token)