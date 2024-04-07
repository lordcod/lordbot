
from typing import List, Optional
import nextcord
import jmespath
from nextcord.ui import Button
from bot.resources.info import COUNT_ROLES_PAGE
from bot.databases.handlers.guildHD import GuildDateBases
from bot.views import menus
from bot.databases.varstructs import RoleShopPayload


class ShopAcceptView(nextcord.ui.View):
    def __init__(
        self,
        index: int,
        data: RoleShopPayload,
        roles: List[List[RoleShopPayload]]
    ) -> None:
        super().__init__(timeout=None)

        self.role_index = index
        self.data = data
        self.roles = roles

        role_description = data.get(
            "description")+"\n\n" if data.get("description") else ""
        self.embed = nextcord.Embed(
            title=data.get('name') or f"Role #{roles[index].index(data)+1}",
            description=(
                f"{role_description}"
                f"・Role: <@&{data.get('role_id')}>\n"
                f"・Amount: {data.get('amount')}{self.economy_settings.get('emoji')}\n"
                f"・Purchase limit: {data.get('limit', '∞')}"
            )
        )

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        view = EconomyShopView(interaction.guild, self.roles, self.role_index)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.green)
    async def accept(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        pass


class EcnonmyShopDropdown(nextcord.ui.StringSelect):
    def __init__(
        self,
        index: int,
        data: List[RoleShopPayload],
        roles: List[List[RoleShopPayload]]
    ) -> None:
        self.data = data
        self.role_index = index
        self.all_roles = roles
        options = [
            nextcord.SelectOption(
                label=role.get('name') or f"Role #{num}",
                value=role.get('role_id'),
                description=role.get('description')
            )
            for num, role in enumerate(data, start=1+index*COUNT_ROLES_PAGE)
        ]

        super().__init__(placeholder="Select an item", options=options)

        if 0 >= len(options):
            self.add_option(label="Option")
            self.disabled = True

    async def callback(self, interaction: nextcord.Interaction) -> None:
        role_id = self.values[0]
        role_data: RoleShopPayload = jmespath.search(
            f'[?role_id==`{role_id}`]|[0]', self.data)

        if role_data.get('limit') and role_data.get('using_limit', 0) >= role_data.get('limit'):
            await interaction.response.send_message(
                f"The entire limit is exhausted!", ephemeral=True)
            return

        if role_id in interaction.user._roles:
            await interaction.response.send_message(
                f"You already have this role!", ephemeral=True)
            return

        view = ShopAcceptView(self.role_index, self.data, self.all_roles)
        await interaction.response.edit_message(embed=view.embed, view=view)


class EconomyShopView(menus.Main):
    value: List[List[RoleShopPayload]]

    def __init__(
        self,
        guild: nextcord.Guild,
        roles: List[List[RoleShopPayload]],
        index: Optional[int] = None
    ):
        self.guild = guild
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings')

        super().__init__(roles)

        self.index = index if index else self.index
        self.add_item(self.get_shop_dropdown())
        self.remove_item(self.button_previous)
        self.remove_item(self.button_next)

    @property
    def embed(self) -> nextcord.Embed:
        embed = nextcord.Embed(
            title=f"The {self.guild.name} Item Store",
            description="Select the item you want to buy."
        )
        for num, role in enumerate(self.value[self.index], start=1+COUNT_ROLES_PAGE*self.index):
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
        return EcnonmyShopDropdown(self.index, self.value[self.index], self.value)

    async def callback(self, button: Button, interaction: nextcord.Interaction):
        view = self.__class__(interaction.guild, self.value, self.index)
        await interaction.response.edit_message(embed=view.embed, view=view)
