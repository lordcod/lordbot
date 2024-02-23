import nextcord
from bot.databases import GuildDateBases
import re
from bot.views import settings_menu
from ._view import DefaultSettingsView
from bot.resources.info import DEFAULT_COLOR
from bot.languages import i18n


class Modal(nextcord.ui.Modal):
    def __init__(self, guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)

        color = self.gdb.get("color")
        hex_color = f"#{color:0>6x}".upper()

        super().__init__("Color")

        self.color = nextcord.ui.TextInput(
            label="Color", placeholder=hex_color)

        self.add_item(self.color)

    async def callback(self, interaction: nextcord.Interaction):
        locale = self.gdb.get('language')

        hex_color = self.color.value
        if not (result := re.fullmatch(r"#?([0-9a-fA-F]{6})", hex_color)):
            await interaction.response.send_message(i18n.t(locale, 'settings.color.not-valid'),
                                                    ephemeral=True)
            return

        color = int(result.group(1), 16)
        self.gdb.set("color", color)

        view = ColorView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class ColorView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        locale = gdb.get("language")
        color = gdb.get("color")
        hex_color = f"#{color:0>6x}".upper()

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.color.title'),
            description=i18n.t(locale, 'settings.color.description'),
            color=color,
        )
        self.embed._fields = [
            {"name": i18n.t(locale, 'settings.color.current', hex_color=hex_color),
             "value": ""}
        ]

        super().__init__()

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.edit.label = i18n.t(locale, 'settings.button.edit')
        self.reset.label = i18n.t(locale, 'settings.button.reset')

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label="Edit", style=nextcord.ButtonStyle.blurple)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        modal = Modal(interaction.guild_id)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label="Reset", style=nextcord.ButtonStyle.success)
    async def reset(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        gdb = GuildDateBases(interaction.guild_id)
        gdb.set("color", DEFAULT_COLOR)

        view = ColorView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
