import nextcord

from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases
from . import settings



class SetDropdown(nextcord.ui.Select):
    def __init__(self):
        
        options = [
            nextcord.SelectOption(
                label="Economy", emoji=Emoji.economy, value='Economy'
            ),
            nextcord.SelectOption(
                label="Languages", emoji=Emoji.languages, value='Languages'
            ),
            nextcord.SelectOption(
                label="Prefix", emoji=Emoji.prefix, value='Prefix'
            ),
            nextcord.SelectOption(
                label="Color", emoji=Emoji.colour, value='Color'
            ),
            
            nextcord.SelectOption(
                label="Auto Reactionsⁿᵉʷ", emoji=Emoji.reactions, value='Reactions'
            ),
            # nextcord.SelectOption(
            #     label="Auto Translateⁿᵉʷ", emoji=Emoji.auto_translate, value='Auto_Translate'
            # ),
            nextcord.SelectOption(
                label="Auto Thread-Forum Messageⁿᵉʷ", emoji=Emoji.thread_message, value='Thread_Message'
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
    embed = None
    
    def __init__(self,member: nextcord.Member) -> None:
        gdb = GuildDateBases(member.guild.id)
        colour = gdb.get('color')
        
        self.embed = nextcord.Embed(
            description='Взаимодействуйте с выпадающим меню выбора, чтобы настроить сервер.',
            color=colour
        )
        self.embed.set_author(name='Настройка модулей бота.',icon_url=member.guild.icon)
        self.embed.set_footer(text=f'Запрос от {member.display_name}',icon_url=member.avatar)
        
        
        super().__init__()
        
        self.add_item(SetDropdown())