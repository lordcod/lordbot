import nextcord

from  .. import thread_message

from bot.databases.db import GuildDateBases
from bot.languages.settings import (
    thread as thread_langs
)


class ModalBuilder(nextcord.ui.Modal):
    def __init__(self,guild_id,channel_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        self.channel_id = channel_id
        super().__init__(thread_langs.modal.title.get(locale))
        
        self.content = nextcord.ui.TextInput(
            label=thread_langs.modal.label.get(locale),
            placeholder=thread_langs.modal.placeholder.get(locale)
        )
        
        self.add_item(self.content)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        forum_message = gdb.get('thread_messages',{})
        
        content = self.content.value
        channel_id = self.channel_id
        
        forum_message[channel_id] = {}
        forum_message[channel_id]['content'] = content
        
        gdb.set('thread_messages',forum_message)

        view = thread_message.AutoThreadMessage(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)