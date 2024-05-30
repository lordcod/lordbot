import nextcord

from bot.languages import help as help_info
from bot.databases import GuildDateBases
from bot.misc.utils import to_async


@to_async
class HelpDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = await self.gdb.get('language')

        options = [
            nextcord.SelectOption(
                label=help_info.categories_name.get(category).get(locale),
                value=category,
                emoji=help_info.categories_emoji.get(category),
            )
            for category in help_info.categories.keys()
        ]

        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        color = await self.gdb.get('color')
        locale = await self.gdb.get('language')

        category_key = self.values[0]
        category_data = help_info.categories.get(category_key)
        category_name = (f"{help_info.categories_emoji.get(category_key)}"
                         f"{help_info.categories_name.get(category_key).get(locale)}")

        text = ''
        for command in category_data:
            text += f"`{command.get('name')}` - {command.get('brief_descriptrion').get(locale)}\n"

        embed = nextcord.Embed(
            title=category_name,
            description=text,
            color=color
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


@to_async
class HelpView(nextcord.ui.View):
    async def __init__(self, guild_id) -> None:
        super().__init__()

        HDD = await HelpDropDown(guild_id)

        self.add_item(HDD)
