import nextcord


class Color(nextcord.ui.Modal):
    type = 'modal'
    def __init__(self) -> None:
        super().__init__("Rewards", timeout=300)
        
        self.color = nextcord.ui.TextInput(
            label='Color',
            placeholder='#2596be'
        )
        
        self.add_item(self.color)
    
    async def callback(self, interaction: nextcord.Interaction) :
        color = self.color.value
        
        await interaction.response.send_message(color,ephemeral=True)

