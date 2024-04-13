import asyncio
import nextcord
from nextcord.ext import commands

from bot.misc.lordbot import LordBot

nextcord.ui.Button.to_component_dict


class interactions_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        bot.set_event(self.on_interaction)
        super().__init__()

    async def dis_interaction_failed(self, interaction: nextcord.Interaction):
        if interaction.type not in (2, 3, 5):
            return
        await asyncio.sleep(2.5-self.bot.latency)
        if interaction.response.is_done():
            return

        embed = nextcord.Embed(
            title="The interaction time has expired",
            description="If you need to use the interaction, call the associated command"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_interaction(self, interaction: nextcord.Interaction):
        self.bot.loop.create_task(self.dis_interaction_failed(interaction))
        await self.bot.process_application_commands(interaction)


def setup(bot):
    bot.add_cog(interactions_event(bot))
