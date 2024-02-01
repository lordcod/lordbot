import nextcord
from nextcord.ext import commands



class interactions_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        
        bot.event(self.on_interaction)
    
    async def on_interaction(self, interaction: nextcord.Interaction):
        await self.bot.process_application_commands(interaction)



def setup(bot: commands.Bot):
    event = interactions_event(bot)
    
    bot.add_cog(event)