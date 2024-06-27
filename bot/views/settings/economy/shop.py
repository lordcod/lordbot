
import nextcord
import jmespath
from bot.databases import GuildDateBases
from bot.databases.varstructs import RoleShopPayload
from typing import List, Optional
from copy import deepcopy

from bot.misc.utils import to_async
from .. import economy
from .._view import DefaultSettingsView


def get_role_data(role_id: int, roles: List[RoleShopPayload]) -> RoleShopPayload:
    return jmespath.search(
        f'[?role_id==`{role_id}`]|[0]', roles)


def update_role_data(
    role_data: RoleShopPayload,
    roles: List[RoleShopPayload]
) -> List[RoleShopPayload]:
    roles = roles or []
    new_roles = deepcopy(roles)
    for index, rd in enumerate(roles):
        if rd.get('role_id') != role_data.get('role_id'):
            continue
        new_roles[index] = role_data
        break
    else:
        new_roles.append(role_data)
    return new_roles


@to_async
class ShopModal(nextcord.ui.Modal):
    async def __init__(self, guild_id: int, role_id: int) -> None:
        self.role_id = role_id
        self.gdb = GuildDateBases(guild_id)
        economy_settings = await self.gdb.get('economic_settings', {})
        shop_info = economy_settings.get('shop')
        self.role_data = role_data = get_role_data(role_id, shop_info) or {}

        super().__init__("Shop role")

        self.amount = nextcord.ui.TextInput(
            label="Amount",
            custom_id="shop:amount",
            max_length=6,
            placeholder=role_data.get('amount')
        )
        if role_data.get('amount'):
            self.amount.required = False
        self.add_item(self.amount)

        self.limit = nextcord.ui.TextInput(
            label="Limit",
            custom_id="shop:limit",
            max_length=3,
            placeholder=role_data.get('limit'),
            required=False
        )
        self.add_item(self.limit)

        self.name = nextcord.ui.TextInput(
            label="Name",
            custom_id="shop:name",
            max_length=100,
            placeholder=role_data.get('name'),
            required=False
        )
        self.add_item(self.name)

        self.description = nextcord.ui.TextInput(
            label="Description",
            custom_id="shop:description",
            style=nextcord.TextInputStyle.paragraph,
            placeholder=role_data.get('description'),
            required=False
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        if not self.amount.value.isdigit():
            await interaction.response.send_message("Amout is invalid format!")
            return
        if self.limit.value and not self.limit.value.isdigit():
            await interaction.response.send_message("Limit is invalid format!")
            return

        economy_settings = await self.gdb.get('economic_settings', {})
        shop_info = economy_settings.get('shop')

        if not self.role_data:
            self.role_data = {
                "role_id": self.role_id,
                "amount": int(self.amount.value),
                "limit": self.limit.value and int(self.limit.value),
                "name": self.name.value,
                "description": self.description.value
            }
        else:
            self.role_data = {
                "role_id": self.role_id,
                "amount": int(self.amount.value) or self.role_data.get('amount'),
                "limit": self.limit.value and int(self.limit.value) or self.role_data.get('limit'),
                "name": self.name.value or self.role_data.get('name'),
                "description": self.description.value or self.role_data.get('description'),
                "using_limit":  self.role_data.get('using_limit')
            }
        shop_info = update_role_data(self.role_data, shop_info)
        economy_settings['shop'] = shop_info
        await self.gdb.set('economic_settings', economy_settings)

        view = await ShopView(interaction.guild,
                              interaction.guild.get_role(self.role_id))
        await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class ShopDropDown(nextcord.ui.RoleSelect):
    async def __init__(self, guild_id):
        self.gdb = GuildDateBases(guild_id)
        super().__init__(
            placeholder="Setting up shop roles",
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        role = self.values[0]
        if role.is_default():
            await interaction.response.send_message(
                content=f"The {role.mention} role is the default role for all users and can't be selected.",
                ephemeral=True
            )
        elif role.is_premium_subscriber():
            await interaction.response.send_message(
                content=f"The {role.mention} role is a role that is used by subscribers of your server.",
                ephemeral=True
            )
        elif role.is_integration() or role.is_bot_managed():
            await interaction.response.send_message(
                content=f"The {role.mention} role cannot be assigned and is used for integration or by a bot.",
                ephemeral=True
            )
        elif role.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message(
                content=f"The bot will not be able to assign the role {role.mention}, as that role is lower than the bot's. To resolve this issue, please move the role {interaction.guild.self_role.mention} to a higher position than {role.mention}.",
                ephemeral=True
            )
        else:
            view = await ShopView(interaction.guild, role)
            await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class ShopView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild, selected_role: Optional[nextcord.Role] = None) -> None:
        self.selected_role = selected_role
        self.gdb = GuildDateBases(guild.id)
        economy_settings = await self.gdb.get('economic_settings')
        shop_info = economy_settings.get('shop', [])
        super().__init__()

        dd = await ShopDropDown(guild.id)
        self.add_item(dd)

        if selected_role and (data := get_role_data(selected_role.id, shop_info)):
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
            self.edit.disabled = False
            self.delete.disabled = False
        if selected_role and not get_role_data(selected_role.id, shop_info):
            self.create.disabled = False

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await economy.Economy(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Create", style=nextcord.ButtonStyle.success, disabled=True)
    async def create(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        modal = await ShopModal(interaction.guild_id, self.selected_role.id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Edit", style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        modal = await ShopModal(interaction.guild_id, self.selected_role.id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        economy_settings = await self.gdb.get('economic_settings')
        shop_info: list = economy_settings.get('shop', [])
        role_data = get_role_data(self.selected_role.id, shop_info)
        shop_info.remove(role_data)
        economy_settings['shop'] = shop_info
        await self.gdb.set('economic_settings', economy_settings)

        view = await ShopView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
