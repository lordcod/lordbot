import nextcord
from bot.views import menus
from bot.misc.yandex_api import Track
from typing import List

class CustomList(menus.Main):
    dem = nextcord.Embed(title='Описание',description='Нашего персонала')
    
    async def callback(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gem = self.dem
        gem._fields = [self.value[self.index]]
        await interaction.message.edit(embed=gem,view=self)

class IdeaModal(nextcord.ui.Modal):
    def __init__(self,channel: nextcord.TextChannel):
        super().__init__(
            "Idea",
            timeout=5 * 60,  # 5 minutes
        )
        self.channel = channel

        self.idea = nextcord.ui.TextInput(
            label="Расскажите нам о своей идее",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Постарайтесь описать свою идею как можно более подробно с примерами использования.",
            min_length=10,
            max_length=1800,
        )
        self.add_item(self.idea)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        idea = self.idea.value
        embed = nextcord.Embed(
            title='Новая идея!',
            description='Будет идея или нет, зависит от вас!',
            color=0x7cc0d8
        )
        embed.add_field(name='Идея:',value=idea)
        mes = await self.channel.send(embed=embed)
        await mes.add_reaction("<a:tickmark:1170029771040759969>")
        await mes.add_reaction("<a:cross:1170029921314279544>")
        await mes.create_thread(name="Обсуждение")

class PersistentView(nextcord.ui.View):
    def __init__(self,bot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Предложить", style=nextcord.ButtonStyle.green, custom_id="persistent_view:sug"
    )
    async def green(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel = self.bot.get_channel(1170031835728859208)
        await interaction.response.send_modal(modal=IdeaModal(channel))


