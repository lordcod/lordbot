import random
import string
from typing import List, Optional
import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.languages import i18n
from bot.misc.lordbot import LordBot
from bot.misc.noti.ytypes import Channel
from bot.misc.utils import AsyncSterilization, generate_message
from bot.resources.info import DEFAULT_YOUTUBE_MESSAGE
from bot.views.information_dd import get_info_dd
from bot.views.settings import notification
from bot.views.settings._view import DefaultSettingsView


def generate_hex(): return ''.join([random.choice(string.hexdigits) for _ in range(18)])


@AsyncSterilization
class YoutubeMessageModal(nextcord.ui.Modal):
    embed = None

    async def __init__(self, guild: nextcord.Guild, selected_id: str, data: dict):
        self.selected_id = selected_id
        self.data = data

        super().__init__('Youtube')

        self.message = nextcord.ui.TextInput(
            label='Message',
            placeholder='You can use embed-builder to create a message.',
            style=nextcord.TextInputStyle.paragraph
        )
        self.add_item(self.message)

    async def callback(self, interaction: nextcord.Interaction[LordBot]) -> None:
        await interaction.response.defer()

        message = self.message.value
        self.data['message'] = message

        view = await YoutubeItemView(interaction.guild, self.selected_id, self.data)
        await interaction.message.edit(embed=view.embed, view=view)


@AsyncSterilization
class YoutubeChooseDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild: nextcord.Guild, values: List[Channel], selected_id: Optional[str] = None, data: Optional[dict] = None) -> None:
        self.selected_id = selected_id
        self.data = data
        self.channels = values
        options = [
            nextcord.SelectOption(
                label=ch.name,
                value=ch.id,
                description=ch.custom_url,
                default=data and data['yt_id'] == ch.id
            )
            for ch in values
        ]
        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]

        if self.data is None:
            self.data = {'id': generate_hex()}

        self.data['yt_id'] = value
        for ch in self.channels:
            if ch.id == value:
                self.data['yt_name'] = ch.name
                break

        view = await YoutubeChooseView(interaction.guild, self.channels, self.data['id'], self.data)
        await interaction.message.edit(embed=view.embed, view=view)


@AsyncSterilization
class YoutubeChooseView(nextcord.ui.View):
    embed = None

    async def __init__(self, guild: nextcord.Guild, values: List[Channel], selected_id: Optional[str] = None, data: Optional[dict] = None) -> None:
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')

        self.selected_id = selected_id
        self.data = data
        self.channels = values

        if data is not None:
            selected_channel = nextcord.utils.get(values, id=data['yt_id'])
        else:
            selected_channel = None

        self.embed = nextcord.Embed(
            title='Youtube Notifications',
            color=color,
            description='Get instant updates for new videos from your favorite YouTube channels.',
        )

        super().__init__()

        if selected_channel is not None:
            self.embed.set_thumbnail(selected_channel.thumbnail)
            self.confirm.disabled = False

        self.add_item(await YoutubeChooseDropDown(guild, values, selected_id, data))

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await YoutubeView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Confirm', style=nextcord.ButtonStyle.success, disabled=True)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await YoutubeItemView(interaction.guild, self.data['id'], self.data)
        await interaction.message.edit(embed=view.embed, view=view)


@AsyncSterilization
class YoutubeItemModal(nextcord.ui.Modal):
    embed = None

    async def __init__(self, guild: nextcord.Guild, selected_id: Optional[str] = None, data: Optional[dict] = None):
        self.selected_id = selected_id
        self.data = data

        super().__init__('Youtube')

        self.username = nextcord.ui.TextInput(
            label='Name',
            placeholder='Enter the name or link of the youtuber.'
        )
        self.add_item(self.username)

    async def callback(self, interaction: nextcord.Interaction[LordBot]) -> None:
        await interaction.response.defer()

        gdb = GuildDateBases(interaction.guild_id)
        youtube_data = await gdb.get('youtube_notification')
        if self.data is None and self.selected_id is not None:
            self.data = youtube_data.get(self.selected_id)

        username = self.username.value

        channels = await interaction.client.ytnoti.get_channel_ids_additionally(username)
        if not channels:
            await interaction.followup.send('The channels was not found.')
            return

        view = await YoutubeChooseView(interaction.guild, channels, self.selected_id, self.data)
        await interaction.message.edit(embed=view.embed, view=view)


@AsyncSterilization
class YoutubeChannelDropDown(nextcord.ui.ChannelSelect):
    async def __init__(self, guild: nextcord.Guild, selected_id: str, data: dict):
        self.selected_id = selected_id
        self.data = data

        super().__init__()

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]
        self.data['channel_id'] = channel.id
        view = await YoutubeItemView(interaction.guild, self.selected_id, self.data)
        await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class YoutubeItemView(nextcord.ui.View):
    embed = None

    async def __init__(self, guild: nextcord.Guild, selected_id: str, data: Optional[dict] = None):
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')
        youtube_data = await gdb.get('youtube_notification')

        if selected_id in youtube_data and not data:
            data = youtube_data[selected_id]

        self.selected_id = selected_id
        self.data = data

        if 'yt_id' in data:
            cid: int = data['yt_id']
            bot: LordBot = guild._state._get_client()

            if cid in bot.ytnoti.user_info:
                userinfo = bot.ytnoti.user_info[cid]

            response = await bot.ytnoti.get_channel_ids([cid])
            if len(response) == 0:
                userinfo = None
            else:
                userinfo = response[0]
        else:
            userinfo = None

        user = f'{userinfo.name} ({userinfo.id})' if userinfo else 'unspecified'

        self.embed = nextcord.Embed(
            title='Youtube Notifications',
            color=color,
            description='Get instant updates for new videos from your favorite YouTube channels.',
        )
        self.embed.set_thumbnail(userinfo.thumbnail if userinfo else None)
        self.embed.add_field(
            name='',
            value=(
                f"> User: **{user}**\n"
                f"> Channel: {channel.mention if (channel := guild.get_channel(data.get('channel_id'))) else 'unspecified'}"
            )
        )

        super().__init__()

        if (('channel_id' in data and 'yt_id' in data)
            and (selected_id not in youtube_data
                 or data != youtube_data[selected_id])):
            self.edit.disabled = False

        if selected_id in youtube_data:
            self.delete.disabled = False

        self.add_item(await YoutubeChannelDropDown(guild, selected_id, data))

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await YoutubeView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Update', style=nextcord.ButtonStyle.green, row=1, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction[LordBot]):
        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('youtube_notification', self.selected_id, self.data)

        await interaction.client.ytnoti.add_channel(interaction.guild_id, self.data['yt_id'])

        view = await YoutubeItemView(interaction.guild, self.selected_id)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=1, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        youtube_data = await gdb.get('youtube_notification')
        youtube_data.pop(self.selected_id, None)
        await gdb.set('youtube_notification', youtube_data)

    @nextcord.ui.button(label='Preview message', style=nextcord.ButtonStyle.success, row=2)
    async def view_message(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        message = self.data.get('message', DEFAULT_YOUTUBE_MESSAGE)
        data = await generate_message(message)
        await interaction.response.send_message(**data, ephemeral=True)

    @nextcord.ui.button(label='Change message', style=nextcord.ButtonStyle.blurple, row=2)
    async def change_message(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await YoutubeMessageModal(interaction.guild, self.selected_id, self.data)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Chnage youtuber', style=nextcord.ButtonStyle.grey, row=2)
    async def change_username(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await YoutubeItemModal(interaction.guild, self.selected_id, self.data)
        await interaction.response.send_modal(modal)


@AsyncSterilization
class YoutubeItemsDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        youtube_data = await gdb.get('youtube_notification')

        options = [
            nextcord.SelectOption(
                label=f"{data['yt_name']} ({data['yt_id']})",
                value=id,
                description=str(channel)
            )
            for id, data in youtube_data.items()
            if (channel := guild.get_channel(data['channel_id']))
        ]
        disabled = len(options) == 0
        if disabled:
            options.append(nextcord.SelectOption(label='SelectOption'))
        super().__init__(options=options, disabled=disabled)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]

        view = await YoutubeItemView(interaction.guild, value)
        await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class YoutubeView(DefaultSettingsView):
    embed = None

    async def __init__(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')
        locale = await gdb.get('language')

        self.embed = nextcord.Embed(
            title='Youtube Notifications',
            color=color,
            description='Get instant updates for new videos from your favorite YouTube channels.',
        )

        super().__init__()

        self.add_item(await YoutubeItemsDropDown(guild))

        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await notification.NotificationView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Add', style=nextcord.ButtonStyle.green)
    async def add(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await YoutubeItemModal(interaction.guild)
        await interaction.response.send_modal(modal)
