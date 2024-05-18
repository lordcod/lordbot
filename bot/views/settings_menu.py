import nextcord
from bot.misc.utils import to_async
from bot.resources.ether import Emoji
from bot.databases import GuildDateBases
from bot.views.settings import moduls
from bot.views.settings._view import DefaultSettingsView
from bot.languages import i18n


@to_async
class SetDropdown(nextcord.ui.Select):
    def __ainit__(self, guild_id):
        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')

        options = [
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.economy'),
                emoji=Emoji.economy,
                value='Economy'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.languages'),
                emoji=Emoji.languages,
                value='Languages'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.prefix'),
                emoji=Emoji.prefix,
                value='Prefix'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.color'),
                emoji=Emoji.color,
                value='Color'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.music'),
                emoji=Emoji.channel_voice,
                value='Music'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.auto-roles'),
                emoji=Emoji.auto_role,
                value='AutoRoles'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.role-reactions'),
                emoji=Emoji.auto_role,
                value='RoleReactions'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.welcomer'),
                emoji=Emoji.frame_person,
                value='Welcomer'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.reactions'),
                emoji=Emoji.reactions,
                value='Reactions'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.thread'),
                emoji=Emoji.thread_message,
                value='ThreadMessage'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.logs'),
                emoji=Emoji.frame_person,
                value='Logs'
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.module-name.ideas'),
                emoji=Emoji.lightbulb,
                value='Ideas'
            ),
            nextcord.SelectOption(
                label=i18n.t(
                    locale, 'settings.module-name.command-permission'),
                emoji=Emoji.command,
                value='CommandPermission'
            ),
        ]

        super().__init__(
            placeholder=i18n.t(locale, 'settings.start.choose'),
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        value = self.values[0]
        view = moduls[value](interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)


class SettingsView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, member: nextcord.Member) -> None:
        gdb = GuildDateBases(member.guild.id)
        color = gdb.get('color')
        locale = gdb.get('language')

        self.embed = nextcord.Embed(
            description=i18n.t(locale, 'settings.start.description'),
            color=color
        )
        self.embed.set_author(name=i18n.t(
            locale, 'settings.start.title'), icon_url=member.guild.icon)
        self.embed.set_footer(
            text=i18n.t(locale, 'settings.start.request',
                        name=member.display_name),
            icon_url=member.avatar)

        super().__init__()

        sd = SetDropdown(member.guild.id)
        self.add_item(sd)
