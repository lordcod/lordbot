
from enum import IntEnum
import nextcord
import time

from typing import Dict, Optional

import re
import jmespath
from bot.misc import logstool
from bot.misc.time_transformer import display_time
from bot.misc.utils import to_async
from bot.resources.ether import Emoji
from bot.databases.varstructs import IdeasPayload
from bot.databases import MongoDB, GuildDateBases
from bot.languages import i18n


REGEXP_URL = re.compile(r'https?:\/\/(.+)')

timeout_data: Dict[int, Dict[int, float]] = {}


def get_ban(ideas: IdeasPayload, member_id: int) -> list | None:
    ban_users = ideas.get('ban_users', [])
    data_ban = jmespath.search(
        f"[?@[0]==`{member_id}`]|[0]", ban_users)
    return data_ban


def get_mute(ideas: IdeasPayload, member_id: int) -> list | None:
    muted_users = ideas.get('muted_users', [])
    data_mute = jmespath.search(
        f"[?@[0]==`{member_id}`]|[0]", muted_users)
    return data_mute


class ReactionSystemType(IntEnum):
    REACTIONS = 0
    BUTTONS = 1


class Timeout:
    @staticmethod
    def get(guild_id: int, member_id: int) -> Optional[float]:
        timeout_data.setdefault(guild_id, {})
        return timeout_data[guild_id].get(member_id)

    @staticmethod
    def set(guild_id: int, member_id: int, delay: float) -> None:
        timeout_data.setdefault(guild_id, {})
        timeout_data[guild_id][member_id] = time.time() + delay

    @staticmethod
    def check_usage(guild_id: int, member_id: int) -> bool:
        return time.time() > Timeout.get(guild_id, member_id)


@to_async
class ConfirmModal(nextcord.ui.Modal):
    async def __init__(self, guild_id: int):
        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')

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
        locale = await gdb.get('language')
        ideas_data = await gdb.get('ideas')
        idea_type_reaction = ideas_data.get('reaction_system', 0)
        channel_approved_id = ideas_data.get('channel_approved_id')

        mdb = MongoDB('ideas')
        idea_data = await mdb.get(interaction.message.id)
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
            value=idea_content,
            inline=False
        )
        if reason:
            embed.add_field(
                name=i18n.t(locale, 'ideas.confirm-modal.reason'),
                value=reason,
                inline=False
            )
        embed.set_footer(
            text=i18n.t(locale, 'ideas.confirm-modal.approve',
                        name=interaction.user.display_name),
            icon_url=interaction.user.display_avatar)

        if idea_type_reaction == ReactionSystemType.REACTIONS:
            view = await ConfirmView(interaction.guild_id)
        elif idea_type_reaction == ReactionSystemType.BUTTONS:
            view = await ReactionConfirmView(interaction.guild_id)
            view.promote.disabled = True
            view.demote.disabled = True
        view.approve.disabled = True

        await interaction.message.edit(content=content, embed=embed, view=view)

        if ideas_data.get('thread_delete') and (thread := interaction.message.thread):
            await thread.delete()

        if channel_approved_id is None:
            return

        approved_channel = interaction.guild.get_channel(channel_approved_id)

        embed.set_author(
            name=idea_author.display_name,
            icon_url=idea_author.display_avatar
        )

        await approved_channel.send(embed=embed)
        await logstool.Logs(interaction.guild).approve_idea(interaction.user, idea_author, idea_content, reason, idea_image)


@to_async
class DenyModal(nextcord.ui.Modal):
    async def __init__(self, guild_id: int) -> None:
        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')

        super().__init__(i18n.t(locale, 'ideas.globals.title'))

        self.reason = nextcord.ui.TextInput(
            label="Argument:",
            required=False,
            style=nextcord.TextInputStyle.paragraph,
            min_length=0,
            max_length=1500,
        )
        self.add_item(self.reason)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        reason = self.reason.value
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        ideas_settings: IdeasPayload = await gdb.get('ideas')
        idea_type_reaction = ideas_settings.get('reaction_system', 0)

        mdb = MongoDB('ideas')
        idea_data = await mdb.get(interaction.message.id)
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
        if reason:
            embed.add_field(
                name="Argument:",
                value=reason,
                inline=False
            )
        embed.set_footer(
            text=i18n.t(locale, 'ideas.confirm-view.refused',
                        name=interaction.user.display_name),
            icon_url=interaction.user.display_avatar)
        embed.set_image(idea_image)

        content = i18n.t(locale, 'ideas.confirm-view.idea-content',
                         mention=idea_author.mention)

        if idea_type_reaction == ReactionSystemType.REACTIONS:
            view = await ConfirmView(interaction.guild_id)
        elif idea_type_reaction == ReactionSystemType.BUTTONS:
            view = await ReactionConfirmView(interaction.guild_id)
            view.promote.disabled = True
            view.demote.disabled = True
        view.deny.disabled = True

        if ideas_settings.get('thread_delete') and (thread := interaction.message.thread):
            await thread.delete()

        await interaction.message.edit(content=content, embed=embed, view=view)


@to_async
class ConfirmView(nextcord.ui.View):
    async def __init__(self, guild_id: Optional[int] = None):
        super().__init__(timeout=None)

        if guild_id is None:
            return

        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')

        self.approve.label = i18n.t(
            locale, 'ideas.confirm-view.button.approve')
        self.deny.label = i18n.t(
            locale, 'ideas.confirm-view.button.deny')

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')

        ideas_data: IdeasPayload = await gdb.get('ideas')
        enabled: bool = ideas_data.get('enabled')

        moderation_role_ids = ideas_data.get('moderation_role_ids', [])
        role_ids = set(interaction.user._roles)
        moderation_roles = set(moderation_role_ids)

        if not enabled:
            await interaction.response.send_message(i18n.t(
                locale, 'ideas.globals.ideas_disabled'), ephemeral=True)
            return False

        if not role_ids & moderation_roles:
            await interaction.response.defer(ephemeral=True)
            return False

        return True

    @nextcord.ui.button(label="Approve",
                        style=nextcord.ButtonStyle.green,
                        custom_id='ideas-confirm:confirm',
                        row=1)
    async def approve(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        modal = await ConfirmModal(interaction.guild_id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Deny",
                        style=nextcord.ButtonStyle.red,
                        custom_id='ideas-confirm:cancel',
                        row=1)
    async def deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await DenyModal(interaction.guild_id)
        await interaction.response.send_modal(modal)


@to_async
class ReactionConfirmView(nextcord.ui.View):
    async def __init__(self, guild_id: int | None = None):
        super().__init__(timeout=None)

        if guild_id is None:
            return

        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')

        self.approve.label = i18n.t(
            locale, 'ideas.confirm-view.button.approve')
        self.deny.label = i18n.t(
            locale, 'ideas.confirm-view.button.deny')

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        custom_id = interaction.data['custom_id']
        if custom_id.startswith("reactions-ideas-confirm:"):
            return True
        return await ConfirmView.interaction_check(self, interaction)

    def change_votes(self) -> None:
        self.promote.label = str(len(self.promoted_data))
        self.demote.label = str(len(self.demoted_data))

    async def save_data(self, message_id) -> None:
        mdb = MongoDB('ideas')
        idea_data = await mdb.get(message_id)
        idea_data.update({
            'promoted': self.promoted_data,
            'demoted': self.demoted_data
        })
        await mdb.set(message_id, idea_data)

    async def load_data(self, message_id) -> None:
        mdb = MongoDB('ideas')
        idea_data = await mdb.get(message_id)
        self.promoted_data = idea_data.get('promoted', [])
        self.demoted_data = idea_data.get('demoted', [])

    async def check_data(self, message_id) -> None:
        promoted_data = getattr(self, "promoted_data", None)
        demoted_data = getattr(self, "demoted_data", None)
        if promoted_data is None or demoted_data is None:
            await self.load_data(message_id)

    @nextcord.ui.button(label="0", emoji="👍", row=2, custom_id="reactions-ideas-confirm:promote")
    async def promote(self, button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        await self.check_data(interaction.message.id)

        if interaction.user.id in self.promoted_data:
            self.promoted_data.remove(interaction.user.id)
        elif interaction.user.id in self.demoted_data:
            self.demoted_data.remove(interaction.user.id)
            self.promoted_data.append(interaction.user.id)
        else:
            self.promoted_data.append(interaction.user.id)

        self.change_votes()

        await self.save_data(interaction.message.id)
        await interaction.response.edit_message(view=self)

    @nextcord.ui.button(label="0", emoji="👎", row=2, custom_id="reactions-ideas-confirm:demote")
    async def demote(self, button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        await self.check_data(interaction.message.id)

        if interaction.user.id in self.demoted_data:
            self.demoted_data.remove(interaction.user.id)
        elif interaction.user.id in self.promoted_data:
            self.promoted_data.remove(interaction.user.id)
            self.demoted_data.append(interaction.user.id)
        else:
            self.demoted_data.append(interaction.user.id)

        self.change_votes()

        await self.save_data(interaction.message.id)
        await interaction.response.edit_message(view=self)

    @nextcord.ui.button(label="Approve",
                        style=nextcord.ButtonStyle.green,
                        custom_id='ideas-confirm:confirm',
                        row=1)
    async def approve(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        modal = await ConfirmModal(interaction.guild_id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Deny",
                        style=nextcord.ButtonStyle.red,
                        custom_id='ideas-confirm:cancel',
                        row=1)
    async def deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await DenyModal(interaction.guild_id)
        await interaction.response.send_modal(modal)


@to_async
class IdeaModal(nextcord.ui.Modal):
    async def __init__(self, guild_id: int):
        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')
        ideas_data: IdeasPayload = await gdb.get('ideas')
        allow_image = ideas_data.get('allow_image', True)

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
        if allow_image:
            self.add_item(self.image)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        color = await gdb.get('color')
        ideas_data: IdeasPayload = await gdb.get('ideas')
        channel_offers_id = ideas_data.get('channel_offers_id')
        cooldown = ideas_data.get('cooldown', 0)
        reaction_type = ideas_data.get(
            'reaction_system', ReactionSystemType.REACTIONS)

        channel = interaction.guild.get_channel(channel_offers_id)
        idea = self.idea.value
        image = self.image.value

        if not (image and REGEXP_URL.fullmatch(image)):
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

        if reaction_type == ReactionSystemType.REACTIONS:
            view = await ConfirmView(interaction.guild_id)
            mes = await channel.send(embed=embed, view=view)
            await mes.add_reaction(Emoji.tickmark)
            await mes.add_reaction(Emoji.cross)
        elif reaction_type == ReactionSystemType.BUTTONS:
            view = await ReactionConfirmView(interaction.guild_id)
            mes = await channel.send(embed=embed, view=view)
        await mes.create_thread(name=i18n.t(locale, 'ideas.idea-modal.thread-name', name=interaction.user.display_name))

        idea_data = {
            'user_id': interaction.user.id,
            'idea': idea,
            'image': image
        }
        mdb = MongoDB('ideas')
        await mdb.set(mes.id, idea_data)

        Timeout.set(interaction.guild_id,
                    interaction.user.id, time.time()+cooldown)
        await logstool.Logs(interaction.guild).create_idea(interaction.user, idea, image)


@to_async
class IdeaView(nextcord.ui.View):
    async def __init__(self, guild_id: int = None):
        super().__init__(timeout=None)

        if guild_id is None:
            return

        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')
        color = await gdb.get('color')

        self.embed = nextcord.Embed(
            title="Ideas",
            description=(
                "Do you have a good idea?\n"
                "And you are sure that everyone will like it!\n"
                "Before you write it, make sure that there have "
                "been no such ideas yet!"
            ),
            color=color
        )

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
        locale = await gdb.get('language')
        ideas_data: IdeasPayload = await gdb.get('ideas')
        enabled: bool = ideas_data.get('enabled', False)
        ban_data = get_ban(ideas_data, interaction.user.id)
        mute_data = get_mute(ideas_data, interaction.user.id)
        user_timeout = Timeout.get(interaction.guild_id, interaction.user.id)

        if not enabled:
            await interaction.response.send_message(i18n.t(locale, 'ideas.globals.ideas-disabled'), ephemeral=True)
            return

        if user_timeout and user_timeout > time.time():
            await interaction.response.send_message(
                content=i18n.t(
                    locale, 'ideas.idea-view.timeout-message', time=int(user_timeout)),
                ephemeral=True
            )
            return

        if ban_data is not None:
            moderator = interaction.guild.get_member(ban_data[1])
            await interaction.response.send_message(
                "You have limited access to creating ideas!\n"
                "Exit Time: Forever\n"
                f"Moderator: {moderator.mention}\n"
                f"Reason: `{ban_data[2]}`",  # type: ignore
                ephemeral=True
            )
            return

        if mute_data is not None:
            moderator = interaction.guild.get_member(mute_data[1])
            await interaction.response.send_message(
                "You have limited access to creating ideas!\n"
                f"Exit Time:  <t:{mute_data[2] :.0f}:f>({display_time(mute_data[2]-time.time())})\n"
                f"Moderator: {moderator.mention}\n"
                f"Reason: `{mute_data[3]}`",  # type: ignore
                ephemeral=True
            )
            return

        modal = await IdeaModal(interaction.guild_id)
        await interaction.response.send_modal(modal)
