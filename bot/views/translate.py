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
            placeholder=i18n.t(locale, 'settings.translate.placeholder'),
            min_values=1,
            max_values=1,
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

    async def callback(self, inter: nextcord.Interaction):
        await inter.response.defer()

        dest = self.values[0]
        result = translator.translate(text=inter.message.content, dest=dest)

        view = TranslateView(inter.guild_id, dest)

        await inter.edit_original_message(content=result.text, view=view)


class TranslateView(nextcord.ui.View):
    def __init__(self, guild_id: int, dest: Optional[str] = None) -> None:
        super().__init__(timeout=None)

        TDD = TranslateDropDown(guild_id, dest)
        self.add_item(TDD)
