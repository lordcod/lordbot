import nextcord
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases
from . import settings
from bot.languages.settings import (
    start as start_langs,
    module_name
)


from .translate import TranslateView


class SetDropdown(nextcord.ui.Select):
    def __init__(self,guild_id):
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        options = [
            nextcord.SelectOption(
                label=module_name.economy.get(locale), emoji=Emoji.economy, value='Economy'
            ),
            nextcord.SelectOption(
                label=module_name.languages.get(locale), emoji=Emoji.languages, value='Languages'
            ),
            nextcord.SelectOption(
                label=module_name.prefix.get(locale), emoji=Emoji.prefix, value='Prefix'
            ),
            nextcord.SelectOption(
                label=module_name.color.get(locale), emoji=Emoji.colour, value='Color'
            ),
            
            nextcord.SelectOption(
                label=module_name.reactions.get(locale), emoji=Emoji.reactions, value='Reactions'
            ),
            # nextcord.SelectOption(
            #     label=module_name.translate.get(locale), emoji=Emoji.auto_translate, value='Auto_Translate'
            # ),
            nextcord.SelectOption(
                label=module_name.thread.get(locale), emoji=Emoji.thread_message, value='Thread_Message'
            ),
        ]

        super().__init__(
            placeholder="Choose settings...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        value = self.values[0]
        view = settings.moduls[value](interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)

class SettingsView(settings.DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self,member: nextcord.Member) -> None:
        gdb = GuildDateBases(member.guild.id)
        colour = gdb.get('color')
        locale = gdb.get('language')
        
        self.embed = nextcord.Embed(
            description=start_langs.description.get(locale),
            color=colour
        )
        self.embed.set_author(name=start_langs.author.get(locale),icon_url=member.guild.icon)
        self.embed.set_footer(text=f'{start_langs.request.get(locale)} {member.display_name}',icon_url=member.avatar)
        
        
        super().__init__()
        
        sd = SetDropdown(member.guild.id)
        self.add_item(sd)



