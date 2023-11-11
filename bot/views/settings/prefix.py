import nextcord



class Prefix(nextcord.ui.Modal):
    type = 'modal'
    
    def __init__(self) -> None:
        super().__init__(title='Префикс')
        
        self.prefix = nextcord.ui.TextInput(
            label='Префикс:',
            placeholder='l.',
            max_length=3
        )
        self.add_item(self.prefix)
    
    async def callback(self, interaction: nextcord.Interaction):
        prefix = self.prefix.value
        await interaction.response.send_message(f'New prefix - `{prefix}`',ephemeral=True)
