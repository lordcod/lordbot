
import nextcord

from bot.databases import GuildDateBases
from bot.resources.info import DEFAULT_EMOJI
from bot.misc.utils import is_emoji

from .. import economy
from .._view import DefaultSettingsView


class Modal(nextcord.ui.Modal):
    def __init__(self, guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        economy_settings: dict = gdb.get('economic_settings')
        emoji = economy_settings.get("emoji")
        super().__init__("Emoji", timeout=300)

        self.emoji = nextcord.ui.TextInput(
            label="Custom Emoji",
            placeholder=emoji,
            max_length=250
        )
        self.add_item(self.emoji)

    async def callback(self, interaction: nextcord.Interaction):
        value = self.emoji.value

        if not is_emoji(value):
            await interaction.response.send_message("You have entered an incorrect emoji", ephemeral=True)
            return

        gdb = GuildDateBases(interaction.guild_id)
        economy_settings = gdb.get('economic_settings')

        economy_settings['emoji'] = value

        gdb.set('economic_settings', economy_settings)

        view = EmojiView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class SelectedEmojiDropDown(nextcord.ui.StringSelect):
    def __init__(self, guild: nextcord.Guild, emoji: str) -> None:
        super().__init__(options=[
            nextcord.SelectOption(
                label="The current emoji",
                emoji=emoji,
                default=True
            )
        ])


class EmojiView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        economy_settings: dict = gdb.get('economic_settings')
        emoji = economy_settings.get("emoji")

        color = gdb.get('color', 1974050)
        self.embed = nextcord.Embed(
            title='Custom emoji',
            description=(
                "You are on the way to creating a good economy.\n"
                "You can set emojis for your economy"
            ),
            color=color
        )

        super().__init__()
        self.add_item(SelectedEmojiDropDown(guild, emoji))

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = economy.Economy(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install', style=nextcord.ButtonStyle.blurple)
    async def install(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        modal = Modal(guild_id=interaction.guild_id)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Reset', style=nextcord.ButtonStyle.success)
    async def reset(self,
                    button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        economy_settings = gdb.get('economic_settings')

        economy_settings['emoji'] = DEFAULT_EMOJI

        gdb.set('economic_settings', economy_settings)

        view = EmojiView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
