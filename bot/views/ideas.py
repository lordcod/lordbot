import nextcord
import timeit

from typing import Optional

from bot.resources.ether import Emoji
from bot.databases.varstructs import IdeasPayload
from bot.databases import MongoDB, GuildDateBases
from bot.languages import i18n


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
            label=i18n.t(locale, 'ideas.globals.reason-label'),
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

        idea_content = idea_data.get('idea')
        idea_author_id = idea_data.get('user_id')

        reason = self.reason.value

        embed = nextcord.Embed(
            title=i18n.t(locale, 'ideas.confrim-modal.embed.title'),
            color=nextcord.Color.green()
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(
            name=i18n.t(locale, 'ideas.confrim-modal.field'),
            value=idea_content
        )

        author = interaction.guild.get_member(idea_author_id)
        content = i18n.t(locale, 'ideas.confrim-modal.content',
                         mention=author.mention)

        views = ConfirmView(interaction.guild_id)
        views.approve.disabled = True
        views.deny.disabled = True

        await interaction.message.edit(content=content, embed=embed, view=views)

        if channel_approved_id is None:
            return

        channel = interaction.guild.get_channel(channel_approved_id)

        embed_accept = nextcord.Embed(
            title=i18n.t(locale, 'ideas.confrim-modal.idea.embed.title'),
            color=nextcord.Color.green()
        )
        embed_accept.add_field(
            name=i18n.t(locale, 'ideas.confrim-modal.idea.embed.field'),
            value=idea_content,
            inline=False
        )
        if reason:
            embed_accept.add_field(
                name=i18n.t(locale, 'ideas.confrim-modal.idea.embed.reason'),
                value=reason,
                inline=False
            )
        embed_accept.set_footer(
            text=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        await channel.send(content=content, embed=embed_accept)


class ConfirmView(nextcord.ui.View):
    def __init__(self, guild_id: Optional[int] = None):
        super().__init__(timeout=None)

        if guild_id is None:
            return

        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        self.approve.label = i18n.t(
            locale, 'ideas.confrim-view.button.approve')
        self.deny.label = i18n.t(
            locale, 'ideas.confrim-view.button.deny')

    @nextcord.ui.button(label="Approve",
                        style=nextcord.ButtonStyle.green,
                        custom_id='ideas-confirm:confirm')
    async def approve(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        ideas_data: IdeasPayload = gdb.get('ideas')
        moderation_role_ids = ideas_data.get('moderation-role-ids', [])
        enabled: bool = ideas_data.get('enabled', False)

        if enabled is False:
            await interaction.response.send_message(i18n.t(
                locale, 'ideas.globals.ideas_disabled'), ephemeral=True)
            return

        role_ids = set(interaction.user._roles)
        moderation_roles = set(moderation_role_ids)
        if not role_ids & moderation_roles:
            await interaction.response.defer(ephemeral=True)
            return

        modal = ConfirmModal(interaction.guild_id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Deny",
                        style=nextcord.ButtonStyle.red,
                        custom_id='ideas-confirm:cancel')
    async def deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)

        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        ideas_data: IdeasPayload = gdb.get('ideas')
        moderation_role_ids = ideas_data.get('moderation-role-ids', [])
        enabled: bool = ideas_data.get('enabled', False)
        if enabled is False:
            await interaction.response.send_message(i18n.t(
                locale, 'ideas.globals.ideas_disabled'), ephemeral=True)
            return

        mdb = MongoDB('ideas')
        idea_data = mdb.get(interaction.message.id)
        if idea_data is None:
            return

        idea_content = idea_data.get('idea')
        idea_author_id = idea_data.get('user_id')

        role_ids = set(interaction.user._roles)
        moderation_roles = set(moderation_role_ids)
        if not (interaction.user.id == idea_author_id
                or role_ids & moderation_roles):
            return

        name = interaction.user.display_name
        embed = nextcord.Embed(
            title=lang_ConfirmView.old_idea.get(locale),
            color=nextcord.Color.red()
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name=i18n.t(
            locale, 'ideas.confrim-view.idea'), value=idea_content)
        embed.set_footer(
            text=f'{lang_ConfirmView.refused.get(locale)} | {name}',
            icon_url=interaction.user.display_avatar)

        author = interaction.guild.get_member(idea_author_id)
        content = i18n.t(locale, 'ideas.confrim-view.idea-content',
                         mention=author.mention)

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

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)

        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        color = gdb.get('color')
        ideas_data = gdb.get('ideas')
        channel_offers_id = ideas_data.get('channel-offers-id')

        channel = interaction.guild.get_channel(channel_offers_id)
        idea = self.idea.value

        embed = nextcord.Embed(
            title=lang_IdeaModal.embed_title.get(locale),
            description=lang_IdeaModal.embed_description.get(locale),
            color=color
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name=i18n.t(
            locale, 'ideas.idea-modal.idea'), value=idea)

        mes = await channel.send(content=interaction.user.mention,
                                 embed=embed,
                                 view=ConfirmView(interaction.guild_id))
        await mes.add_reaction(Emoji.tickmark)
        await mes.add_reaction(Emoji.cross)
        await mes.create_thread(name=i18n.t(locale, 'ideas.idea-modal.thread-name', name=interaction.user.display_name))

        idea_data = {
            'user_id': interaction.user.id,
            'idea': idea
        }
        mdb = MongoDB('ideas')
        mdb.set(mes.id, idea_data)

        Timeout.set(interaction.guild_id,
                    interaction.user.id, timeit.default_timer()+(60*30))


class IdeaView(nextcord.ui.View):
    def __init__(self, guild_id: int = None):
        super().__init__(timeout=None)
        if guild_id is None:
            return
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        self.suggest.label = i18n.t(locale, 'ideas.globals.placeholder')

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
        if user_timeout and user_timeout > timeit.default_timer():
            await interaction.response.send_message(
                content=i18n.t(
                    locale, 'ideas.idea-view.timeout-message', time=int(user_timeout)),
                ephemeral=True
            )
            return

        gdb = GuildDateBases(interaction.guild_id)
        ideas_data: IdeasPayload = gdb.get('ideas')
        enabled: bool = ideas_data.get('enabled', False)
        if enabled is False:
            await interaction.response.send_message(i18n.t(locale, 'ideas.globals.ideas-disabled'), ephemeral=True)
            return

        modal = IdeaModal(interaction.guild_id)
        await interaction.response.send_modal(modal)
