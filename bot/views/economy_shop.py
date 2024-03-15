
from typing import List
import nextcord
from nextcord.ui import Button
from bot.databases.handlers.guildHD import GuildDateBases
from bot.views import menus
from bot.databases.varstructs import RoleShopPayload


class EcnonmyShopDropdown(nextcord.ui.StringSelect):
    def __init__(self, data: List[RoleShopPayload]) -> None:
        options = [
            nextcord.SelectOption(
                label=role.get('name') or f"Role #{num}",
                value=role.get('role_id'),
                description=role.get('description')
            )
            for num, role in enumerate(data, start=1)
        ]

        super().__init__(placeholder="Select an item", options=options)

        if 0 >= len(options):
            self.disabled = True
            self.add_option(label="Option")

    async def callback(self, interaction: nextcord.Interaction) -> None:
        pass


class EconomyShopView(menus.Main):
    value: List[List[RoleShopPayload]]

    def __init__(self, guild: nextcord.Guild, roles):
        self.guild = guild
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings')

        super().__init__(roles)

        self.add_item(self.get_shop_dropdown())
        self.remove_item(self.button_previous)
        self.remove_item(self.button_next)

    @property
    def embed(self) -> nextcord.Embed:
        embed = nextcord.Embed(
            title=f"The {self.guild.name} Item Store",
            description="Select the item you want to buy."
        )
        for num, role in enumerate(self.value[self.index], start=1):
            embed.add_field(
                name=role.get('name') or f"Role #{num}",
                value=(
                    f"・Role: <@&{role.get('role_id')}>\n"
                    f"・Amount: {role.get('amount')}{self.economy_settings.get('emoji')}\n"
                    f"・Purchase limit: {role.get('limit', '∞')}"
                ),
                inline=False
            )
        embed.set_footer(text=f"Page {self.index+1}/{self.len}")
        return embed

    def get_shop_dropdown(self) -> EcnonmyShopDropdown:
        return EcnonmyShopDropdown(self.value[self.index])

    async def callback(self, button: Button, interaction: nextcord.Interaction):
        view = self.__class__(self.value)
        await interaction.response.edit_message(embed=view.embed, view=view)
