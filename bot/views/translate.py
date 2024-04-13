from typing import Optional
import nextcord
from bot import languages
from bot.languages import i18n
from bot.databases import GuildDateBases
import googletrans

translator = googletrans.Translator()


class TranslateDropDown(nextcord.ui.Select):
    def __init__(self, guild_id: int, dest: Optional[str] = None) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        super().__init__(
            placeholder=i18n.t(locale, 'translate.placeholder'),
            options=[
                nextcord.SelectOption(
                    label=lang.get('native_name'),
                    value=lang.get('google_language'),
                    description=lang.get('language_name'),
                    emoji=lang.get('flag'),
                    default=lang.get('google_language') == dest
                )
                for lang in languages.data[:24]
            ]
        )

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()

        dest = self.values[0]
        result = translator.translate(
            text=interaction.message.content, dest=dest)

        view = TranslateView(interaction.guild_id, dest)
        await interaction.edit_original_message(content=result.text, view=view)


class TranslateView(nextcord.ui.View):
    def __init__(self, guild_id: int, dest: Optional[str] = None) -> None:
        super().__init__(timeout=None)
        self.add_item(TranslateDropDown(guild_id, dest))
