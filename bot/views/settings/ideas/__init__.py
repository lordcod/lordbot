import nextcord

from bot.misc.utils import AsyncSterilization

from bot.views.settings._view import DefaultSettingsView
from .distribution import distrubuters

from bot.databases.varstructs import IdeasPayload
from bot.databases import GuildDateBases
from bot.views import settings_menu
from bot.views.ideas import IdeaView
from bot.languages import i18n
from bot.misc.time_transformer import display_time


@AsyncSterilization
class DropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id):
        self.gdb = GuildDateBases(guild_id)
        locale = await self.gdb.get('language')

        options = [
            nextcord.SelectOption(
                label=i18n.t(
                    locale, f'settings.ideas.init.dropdown.{value}.title'),
                value=value,
                description=i18n.t(
                    locale, f'settings.ideas.init.dropdown.{value}.description')
            )
            for value in {'approved', 'mod_roles', 'offers', 'suggest', 'cooldown'}
        ]

        super().__init__(
            placeholder=i18n.t(
                locale, 'settings.ideas.init.dropdown.placeholder'),
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        catalog = self.values[0]
        view = await distrubuters[catalog](interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class IdeasView(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        color: int = await gdb.get('color')
        locale: str = await gdb.get('language')
        ideas: IdeasPayload = await gdb.get('ideas', {})
        enabled = ideas.get('enabled')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.ideas.init.title'),
            description=i18n.t(locale, 'settings.ideas.init.description'),
            color=color
        )

        super().__init__()

        description = ''

        if channel_suggest := guild.get_channel(ideas.get("channel_suggest_id")):
            description += i18n.t(locale, 'settings.ideas.init.value.suggest',
                                  channel=channel_suggest.mention)

        if channel_offers := guild.get_channel(ideas.get("channel_offers_id")):
            description += i18n.t(locale, 'settings.ideas.init.value.offers',
                                  channel=channel_offers.mention)

        if channel_approved := guild.get_channel(
                ideas.get("channel_approved_id")):
            description += i18n.t(locale, 'settings.ideas.init.value.approved',
                                  channel=channel_approved.mention)

        if cooldown := ideas.get('cooldown'):
            description += i18n.t(locale, 'settings.ideas.init.value.cooldown',
                                  cooldown=display_time(cooldown, locale, max_items=2))

        if moderation_role_ids := ideas.get("moderation_role_ids"):
            moderation_roles = filter(lambda item: item is not None,
                                      map(guild.get_role,
                                          moderation_role_ids))
            if moderation_roles:
                description += i18n.t(locale, 'settings.ideas.init.value.mod_roles',
                                      roles=', '.join([role.mention for role in moderation_roles]))

        if description:
            self.embed.add_field(
                name='',
                value=description.removesuffix('\n')
            )

        self.allow_image.style = nextcord.ButtonStyle.green if ideas.get(
            'allow_image', True) else nextcord.ButtonStyle.red
        self.thread_delete.style = nextcord.ButtonStyle.green if ideas.get(
            'thread_delete', True) else nextcord.ButtonStyle.red

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.enable.label = i18n.t(locale, 'settings.button.enable')
        self.disable.label = i18n.t(locale, 'settings.button.disable')
        self.allow_image.label = i18n.t(
            locale, 'settings.ideas.button.allow_image')
        self.thread_delete.label = i18n.t(
            locale, 'settings.ideas.button.thread_delete')

        if enabled:
            self.remove_item(self.enable)
        else:
            self.remove_item(self.disable)
            self.allow_image.disabled = True
            self.thread_delete.disabled = True

        self.add_item(await DropDown(guild.id))

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Enable', style=nextcord.ButtonStyle.blurple)
    async def enable(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        color = await gdb.get('color')
        locale = await gdb.get('language')
        ideas: IdeasPayload = await gdb.get('ideas')

        channel_suggest_id = ideas.get("channel_suggest_id")
        channel_offers_id = ideas.get("channel_offers_id")

        channel_suggest = interaction.guild.get_channel(channel_suggest_id)
        channel_offers = interaction.guild.get_channel(channel_offers_id)

        if not (channel_suggest and channel_offers):
            await interaction.response.send_message(
                i18n.t(locale, 'settings.ideas.init.error.enable'),
                ephemeral=True
            )
            return

        view = await IdeaView(interaction.guild_id)
        message_suggest = await channel_suggest.send(embed=view.embed, view=view)

        ideas['message_suggest_id'] = message_suggest.id
        ideas['enabled'] = True
        await gdb.set('ideas', ideas)

        view = await IdeasView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Disable', style=nextcord.ButtonStyle.red)
    async def disable(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: IdeasPayload = await gdb.get('ideas')

        channel_suggest_id = ideas.get("channel_suggest_id")
        channel_suggest = interaction.guild.get_channel(channel_suggest_id)
        message_suggest_id = ideas.get("message_suggest_id")

        if channel_suggest and message_suggest_id:
            message_suggest = channel_suggest.get_partial_message(
                message_suggest_id)
            try:
                await message_suggest.delete()
            except nextcord.errors.HTTPException:
                pass

        ideas['enabled'] = False

        await gdb.set('ideas', ideas)

        view = await IdeasView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Allow image")
    async def allow_image(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: IdeasPayload = await gdb.get('ideas')
        ideas['allow_image'] = not ideas.get('allow_image', True)
        await gdb.set('ideas', ideas)

        view = await IdeasView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Thread delete")
    async def thread_delete(self,
                            button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: IdeasPayload = await gdb.get('ideas')
        ideas['thread_delete'] = not ideas.get('thread_delete', False)
        await gdb.set('ideas', ideas)

        view = await IdeasView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
