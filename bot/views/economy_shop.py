
from typing import List, Optional
import nextcord
import jmespath
from bot.resources.info import COUNT_ROLES_PAGE
from bot.misc.utils import FissionIterator
from bot.databases import GuildDateBases
from bot.databases import EconomyMemberDB
from bot.views import menus
from bot.databases.varstructs import RoleShopPayload


class ShopAcceptView(nextcord.ui.View):
    def __init__(
        self,
        guild_id: int,
        index: int,
        data: RoleShopPayload
    ) -> None:
        super().__init__(timeout=None)

        self.gdb = GuildDateBases(guild_id)
        economy_settings = self.gdb.get('economic_settings')
        shop_info = economy_settings.get('shop', [])
        self.role_index = index
        self.data = data

        role_description = data.get(
            "description")+"\n\n" if data.get("description") else ""
        role_limit = data.get('limit')-data.get('using_limit',
                                                0) if data.get('limit') else '∞'
        self.embed = nextcord.Embed(
            title=data.get('name') or f"Role #{shop_info.index(data)+1}",
            description=(
                f"{role_description}"
                f"・Role: <@&{data.get('role_id')}>\n"
                f"・Amount: {data.get('amount')}{economy_settings.get('emoji')}\n"
                f"・Purchase limit: {role_limit}"
            )
        )

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        view = EconomyShopView(interaction.guild, self.role_index)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.green)
    async def accept(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        economy_settings = self.gdb.get('economic_settings')
        shop_info = economy_settings.get(
            'shop', [])
        emdb = EconomyMemberDB(interaction.guild_id, interaction.user.id)

        if self.data.get('role_id') in interaction.user._roles:
            await interaction.response.send_message(
                "You already have this role!", ephemeral=True)
            return
        if self.data.get('limit') and self.data.get('using_limit', 0) >= self.data.get('limit'):
            await interaction.response.send_message(
                "The entire limit is exhausted!", ephemeral=True)
            return
        if self.data.get('amount') > emdb.get('balance'):
            await interaction.response.send_message(
                f"Your balance must be more than {self.data.get('amount')}{economy_settings.get('emoji')}",
                ephemeral=True)
            return
        try:
            await interaction.user._state.http.add_role(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id,
                role_id=self.data.get('role_id'),
                reason="Buying a role in the store"
            )
        except nextcord.HTTPException:
            interaction.user.send(
                f"[**{interaction.guild.name}**] Shop role was not found! Contact the server administrators!")
            return
        for rd in shop_info:
            if rd.get('role_id') == self.data.get('role_id'):
                rd['using_limit'] = rd.get('using_limit', 0) + 1
        economy_settings['shop'] = shop_info
        self.gdb.set('economic_settings', economy_settings)
        emdb['balance'] -= self.data.get('amount')

        await interaction.response.send_message(f"You have completed the purchase of the role <@&{self.data.get('role_id')}>",
                                                ephemeral=True)

        view = EconomyShopView(interaction.guild, self.role_index)
        await interaction.response.edit_message(embed=view.embed, view=view)


class EconomyShopDropdown(nextcord.ui.StringSelect):
    def __init__(
        self,
        index: int,
        data: List[RoleShopPayload]
    ) -> None:
        self.data = data
        self.role_index = index

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
        gdb = GuildDateBases(interaction.guild_id)
        economy_settings = gdb.get('economic_settings')
        emdb = EconomyMemberDB(interaction.guild_id, interaction.user.id)
        role_id = int(self.values[0])
        role_data: RoleShopPayload = jmespath.search(
            f'[?role_id==`{role_id}`]|[0]', self.data)

        if role_id in interaction.user._roles:
            await interaction.response.send_message(
                "You already have this role!", ephemeral=True)
            return
        if role_data.get('limit') and role_data.get('using_limit', 0) >= role_data.get('limit'):
            await interaction.response.send_message(
                "The entire limit is exhausted!", ephemeral=True)
            return
        if role_data.get('amount') > emdb.get('balance'):
            await interaction.response.send_message(
                f"Your balance must be more than {role_data.get('amount') :,}{economy_settings.get('emoji')}",
                ephemeral=True)
            return

        view = ShopAcceptView(interaction.guild_id,
                              self.role_index, role_data)
        await interaction.response.edit_message(embed=view.embed, view=view)


class EconomyShopView(menus.Menus):
    value: List[List[RoleShopPayload]]

    def __init__(
        self,
        guild: nextcord.Guild,
        index: Optional[int] = None
    ):
        self.guild = guild
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings')
        shop_info = self.economy_settings.get('shop', [])
        eft = FissionIterator(shop_info, COUNT_ROLES_PAGE).to_list()

        super().__init__(eft)

        self.index = index if index else self.index
        self.add_item(self.get_shop_dropdown())
        self.remove_item(self.button_previous)
        self.remove_item(self.button_next)

        self.handler_disable()

    @property
    def embed(self) -> nextcord.Embed:
        embed = nextcord.Embed(
            title=f"The {self.guild.name} Item Store",
            description="Select the item you want to buy."
        )
        for num, role in enumerate(self.value[self.index], start=1+COUNT_ROLES_PAGE*self.index):
            role_limit = role.get('limit')-role.get('using_limit',
                                                    0) if role.get('limit') else '∞'
            embed.add_field(
                name=role.get('name') or f"Role #{num}",
                value=(
                    f"・Role: <@&{role.get('role_id')}>\n"
                    f"・Amount: {role.get('amount') :,}{self.economy_settings.get('emoji')}\n"
                    f"・Purchase limit: {role_limit}"
                ),
                inline=False
            )
        embed.set_footer(text=f"Page {self.index+1}/{self.len}")
        return embed

    def get_shop_dropdown(self) -> EconomyShopDropdown:
        return EconomyShopDropdown(self.index, self.value[self.index])

    async def callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = self.__class__(interaction.guild, self.index)
        await interaction.response.edit_message(embed=view.embed, view=view)
