import nextcord
from bot.misc.utils import AsyncSterilization
from .base import FunctionOptionItem


@AsyncSterilization
class AllowImageFunc(FunctionOptionItem):
    async def __init__(self, guild: nextcord.Guild):
        await super().__init__(guild)

        ideas = await self.get_ideas_data()
        self.allow_image = ideas.get('allow_image', True)

        if self.allow_image:
            self.label = 'settings.ideas.dropdown.allow_image.disable.label'
            self.description = 'settings.ideas.dropdown.allow_image.disable.description'
            self.emoji = 'ticoff'
        else:
            self.label = 'settings.ideas.dropdown.allow_image.enable.label'
            self.description = 'settings.ideas.dropdown.allow_image.enable.description'
            self.emoji = 'ticon'

    async def callback(self, interaction: nextcord.Interaction) -> None:
        ideas = await self.get_ideas_data()
        ideas['allow_image'] = not ideas.get('allow_image', True)
        await self.set_ideas_data(ideas)

        await super().callback(interaction)
