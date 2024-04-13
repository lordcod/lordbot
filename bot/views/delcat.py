from typing import Any, Coroutine
import nextcord

from bot.resources.ether import Emoji


class DelCatView(nextcord.ui.View):
    def __init__(
        self,
        member: nextcord.Member,
        category: nextcord.CategoryChannel
    ) -> None:
        self.member = member
        self.category = category
        self.embed = nextcord.Embed(
            title=f"{Emoji.warn} Are you sure?",
            description=f"This will permanently delete the {category.mention} category and every channel inside of it.",
            color=0xED390D
        )
        super().__init__()

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.blurple)
    async def accept(
        self,
        button: nextcord.ui.Button,
        interaction: nextcord.Interaction
    ) -> None:
        embed = nextcord.Embed(
            title=f"{Emoji.success} #{self.category.name} Category Deleted",
            description=f"And also remotely {len(self.category.channels)} channels that were in the category",
            color=0x57F287
        )

        for channel in self.category.channels:
            await channel.delete()
        await self.category.delete()

        await interaction.message.edit(embed=embed, view=None)

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def cancel(
        self,
        button: nextcord.ui.Button,
        interaction: nextcord.Interaction
    ) -> None:
        embed = nextcord.Embed(
            title=f"{Emoji.success} Category Deletion Canceled",
            color=0x57F287
        )

        await interaction.message.edit(embed=embed, view=None)

    async def interaction_check(
        self,
        interaction: nextcord.Interaction
    ) -> Coroutine[Any, Any, bool]:
        if interaction.user != self.member:
            return False
        return True
