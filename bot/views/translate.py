import nextcord
from bot import languages
from bot.databases.db import GuildDateBases
import googletrans

translator = googletrans.Translator()


class TranslateDropDown(nextcord.ui.Select):
    def __init__(self, guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        super().__init__(
            placeholder=languages.translate.placeholder.get(locale),
            min_values=1,
            max_values=1,
            options=[
                nextcord.SelectOption(
                    label=lang.get('native_name'),
                    description=lang.get('language_name'),
                    emoji=lang.get('flag'),
                    value=lang.get('google_language')
                )
                for lang in languages.data[:24]
            ]
        )
    
    async def callback(self, inter: nextcord.Interaction):
        await inter.response.defer()
        
        dest = self.values[0]
        result = translator.translate(text=inter.message.content, dest=dest)
        
        await inter.edit_original_message(content=result.text)

class TranslateView(nextcord.ui.View):
    def __init__(self, guild_id) -> None:
        super().__init__(timeout=None)
        
        TDD = TranslateDropDown(guild_id)
        self.add_item(TDD)
