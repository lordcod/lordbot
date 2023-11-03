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
        self.info = nextcord.ui.TextInput(
            label="Information",
            placeholder="The ideas are completely anonymous!",
            required=False,
            min_length=0,
            max_length=2,
        )
        self.add_item(self.info)
        
        self.name = nextcord.ui.TextInput(
            label="Your name?",
            placeholder='It is not necessary to specify the name!',
            required=False,
            min_length=2,
            max_length=50,
        )
        self.add_item(self.name)

        self.idea = nextcord.ui.TextInput(
            label="Tell us your idea",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Try to describe your idea in as much detail as possible with usage examples.",
            min_length=10,
            max_length=1800,
        )
        self.add_item(self.idea)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        username = self.name.value
        idea = self.idea.value
        embed = nextcord.Embed(
            title='A new idea!',
            description='Whether there will be an idea or not is up to you!'
        )
        if username:
            embed.add_field(
                name='Who came up with the idea',
                value=username
            )
        embed.add_field(name='Idea',value=idea)
        mes = await self.channel.send(embed=embed)
        await mes.add_reaction("<a:tickmark:1165684814557495326>")
        await mes.add_reaction("<a:cross:1165684812250611732>")
        await mes.create_thread(name="Discussion")

