import nextcord
from bot.databases.db import GuildDateBases


class Prefix(nextcord.ui.Modal):
    type = 'modal'
    
    def __init__(self,guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        prefix = self.gdb.get('prefix')
        
        super().__init__(title='Префикс')
        
        self.prefix = nextcord.ui.TextInput(
            label='Префикс:',
            placeholder=prefix,
            max_length=7
        )
        self.add_item(self.prefix)
    
    async def callback(self, interaction: nextcord.Interaction):
        prefix = self.prefix.value
        self.gdb.set('prefix',prefix)
        await interaction.response.send_message(f'New prefix - `{prefix}`',ephemeral=True)
