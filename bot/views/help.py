import nextcord

from bot.languages import help as help_info
from bot.databases.db import GuildDateBases

class DropDown(nextcord.ui.Select):
    def __init__(self, guild_id: int) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        
        options = [
            nextcord.SelectOption(
                label=help_info.categories_name.get(category).get(locale),
                value=category
            )
            for category in help_info.categories.keys()
        ]
        
        super().__init__(
            options=options
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        colour = self.gdb.get('color')
        locale = self.gdb.get('language')
        
        category_key = self.values[0]
        category_data = help_info.categories.get(category_key)
        category_name = help_info.categories_name.get(category_key).get(locale)
        
        text = ''
        for command in category_data:
            text = (
                f"{text}"
                f"`{command.get('name')}` - {command.get('brief_descriptrion').get(locale)}"
                "\n"
            )
        
        embed = nextcord.Embed(
            title=category_name,
            description=text,
            color=colour
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpView(nextcord.ui.View):
    def __init__(self, guild_id) -> None:
        super().__init__()
        
        
        HDD = DropDown(guild_id)
        
        self.add_item(HDD)