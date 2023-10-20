""""PersistentView(class)
bot = commands.Bot(command_prefix='.',intents=nextcord.Intents.all())
bot.persistent_views_added = False

@bot.event
async def on_ready():
    if not bot.persistent_views_added:
        bot.add_view(PersistentView())
        bot.persistent_views_added = True
    print(f"The bot is registered as {bot.user}")
"""
