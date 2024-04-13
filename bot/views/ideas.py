
import nextcord
import time

from typing import Optional

import re
from bot.resources.ether import Emoji
from bot.databases.varstructs import IdeasPayload
from bot.databases import MongoDB, GuildDateBases
from bot.languages import i18n


REGEXP_URL = re.compile(r'https?:\/\/(.+)')


@lambda _: _()
class Timeout:
    def __init__(self) -> None:
        self.data = {}

    def get(self, guild_id: int, member_id: int) -> Optional[float]:
        if guild_id not in self.data:
            self.data[guild_id] = {}
        return self.data[guild_id].get(member_id)

    def set(self, guild_id: int, member_id: int, delay: float) -> None:
        if guild_id not in self.data:
            self.data[guild_id] = {}
        self.data[guild_id][member_id] = delay


class ConfirmModal(nextcord.ui.Modal):
    def __init__(self, guild_id: int):
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        super().__init__(i18n.t(locale, 'ideas.globals.title'))

        self.reason = nextcord.ui.TextInput(
            label=i18n.t(locale, 'ideas.confirm-modal.reason'),
            required=False,
            style=nextcord.TextInputStyle.paragraph,
            min_length=0,
            max_length=1500,
        )
        self.add_item(self.reason)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        ideas_data = gdb.get('ideas')
        channel_approved_id = ideas_data.get('channel-approved-id')

        mdb = MongoDB('ideas')
        idea_data = mdb.get(interaction.message.id)
        if idea_data is None:
            return

        idea_image = idea_data.get('image')
        idea_content = idea_data.get('idea')
        idea_author_id = idea_data.get('user_id')
        idea_author = interaction.guild.get_member(idea_author_id)

        reason = self.reason.value

        content = i18n.t(locale, 'ideas.confirm-modal.content',
                         mention=idea_author.mention)

        embed = nextcord.Embed(
            title=i18n.t(locale, 'ideas.confirm-modal.title'),
            color=nextcord.Color.green()
        )
        embed.set_image(idea_image)
        embed.add_field(
            name=i18n.t(locale, 'ideas.confirm-modal.essence'),
            value=idea_content
        )
        embed.set_footer(
            text=i18n.t(locale, 'ideas.confirm-modal.approve',
                        name=interaction.user.display_name),
            icon_url=interaction.user.display_avatar)

        if reason:
            embed.add_field(
                name=i18n.t(locale, 'ideas.confirm-modal.reason'),
                value=reason,
                inline=False
            )

        view = ConfirmView(interaction.guild_id)
        view.approve.disabled = True
        view.deny.disabled = True

        await interaction.message.edit(content=content, embed=embed, view=view)

        if channel_approved_id is None:
            return

        approved_channel = interaction.guild.get_channel(channel_approved_id)

        embed.set_author(
            name=idea_author.display_name,
            icon_url=idea_author.display_avatar
        )

        await approved_channel.send(embed=embed)


class ConfirmView(nextcord.ui.View):
    def __init__(self, guild_id: Optional[int] = None):
        super().__init__(timeout=None)

        if guild_id is None:
            return

        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        self.approve.label = i18n.t(
            locale, 'ideas.confirm-view.button.approve')
        self.deny.label = i18n.t(
            locale, 'ideas.confirm-view.button.deny')

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')

        ideas_data: IdeasPayload = gdb.get('ideas')
        enabled: bool = ideas_data.get('enabled', False)

        moderation_role_ids = ideas_data.get('moderation-role-ids', [])
        role_ids = set(interaction.user._roles)
        moderation_roles = set(moderation_role_ids)

        if enabled is False:
            await interaction.response.send_message(i18n.t(
                locale, 'ideas.globals.ideas_disabled'), ephemeral=True)
            return False

        if not role_ids & moderation_roles:
            await interaction.response.defer(ephemeral=True)
            return False

        return True

    @nextcord.ui.button(label="Approve",
                        style=nextcord.ButtonStyle.green,
                        custom_id='ideas-confirm:confirm')
    async def approve(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        modal = ConfirmModal(interaction.guild_id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Deny",
                        style=nextcord.ButtonStyle.red,
                        custom_id='ideas-confirm:cancel')
    async def deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)

        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')

        mdb = MongoDB('ideas')
        idea_data = mdb.get(interaction.message.id)
        if idea_data is None:
            return

        idea_content = idea_data.get('idea')
        idea_image = idea_data.get('image')
        idea_author_id = idea_data.get('user_id')
        idea_author = interaction.guild.get_member(idea_author_id)

        embed = nextcord.Embed(
            title=i18n.t(locale, 'ideas.confirm-view.title'),
            color=nextcord.Color.red()
        )
        embed.set_author(
            name=idea_author.display_name,
            icon_url=idea_author.display_avatar
        )
        embed.add_field(name=i18n.t(
            locale, 'ideas.confirm-view.idea'), value=idea_content)
        embed.set_footer(
            text=i18n.t(locale, 'ideas.confirm-view.refused',
                        name=interaction.user.display_name),
            icon_url=interaction.user.display_avatar)
        embed.set_image(idea_image)

        content = i18n.t(locale, 'ideas.confirm-view.idea-content',
                         mention=idea_author.mention)

        self.approve.disabled = True
        self.deny.disabled = True

        await interaction.message.edit(content=content, embed=embed, view=self)


class IdeaModal(nextcord.ui.Modal):
    def __init__(self, guild_id: int):
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        super().__init__(i18n.t(locale, 'ideas.globals.title'))

        self.idea = nextcord.ui.TextInput(
            label=i18n.t(locale, 'ideas.idea-modal.label'),
            style=nextcord.TextInputStyle.paragraph,
            placeholder=i18n.t(locale, 'ideas.idea-modal.placeholder'),
            min_length=10,
            max_length=1500
        )
        self.add_item(self.idea)

        self.image = nextcord.ui.TextInput(
            label="Image url",
            style=nextcord.TextInputStyle.short,
            placeholder="If you want, you can attach an image",
            min_length=10,
            max_length=150,
            required=False
        )
        self.add_item(self.image)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        color = gdb.get('color')
        ideas_data = gdb.get('ideas')
        channel_offers_id = ideas_data.get('channel-offers-id')
        cooldown = ideas_data.get('cooldown', 0)

        channel = interaction.guild.get_channel(channel_offers_id)
        idea = self.idea.value
        image = self.image.value

        if not REGEXP_URL.fullmatch(image):
            image = None

        embed = nextcord.Embed(
            title=i18n.t(locale, 'ideas.globals.title'),
            description=i18n.t(locale, 'ideas.idea-modal.embed-description'),
            color=color
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name=i18n.t(
            locale, 'ideas.idea-modal.idea'), value=idea)
        embed.set_image(image)

        mes = await channel.send(embed=embed,
                                 view=ConfirmView(interaction.guild_id))
        await mes.add_reaction(Emoji.tickmark)
        await mes.add_reaction(Emoji.cross)
        await mes.create_thread(name=i18n.t(locale, 'ideas.idea-modal.thread-name', name=interaction.user.display_name))

        idea_data = {
            'user_id': interaction.user.id,
            'idea': idea,
            'image': self.image.value
        }
        mdb = MongoDB('ideas')
        mdb.set(mes.id, idea_data)

        Timeout.set(interaction.guild_id,
                    interaction.user.id, time.time()+cooldown)


class IdeaView(nextcord.ui.View):
    def __init__(self, guild_id: int = None):
        super().__init__(timeout=None)
        if guild_id is None:
            return
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        self.suggest.label = i18n.t(locale, 'ideas.globals.title')

    @nextcord.ui.button(
        label="Suggest an idea",
        style=nextcord.ButtonStyle.green,
        custom_id="ideas-main-button:suggest"
    )
    async def suggest(
        self,
        button: nextcord.ui.Button,
        interaction: nextcord.Interaction
    ) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')

        user_timeout = Timeout.get(interaction.guild_id, interaction.user.id)
        if user_timeout and user_timeout > time.time():
            await interaction.response.send_message(
                content=i18n.t(
                    locale, 'ideas.idea-view.timeout-message', time=int(user_timeout)),
                ephemeral=True
            )
            return

        gdb = GuildDateBases(interaction.guild_id)
        ideas_data: IdeasPayload = gdb.get('ideas')
        enabled: bool = ideas_data.get('enabled')
        if not enabled:
            await interaction.response.send_message(i18n.t(locale, 'ideas.globals.ideas-disabled'), ephemeral=True)
            return

        modal = IdeaModal(interaction.guild_id)
        await interaction.response.send_modal(modal)
