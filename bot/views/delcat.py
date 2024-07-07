import asyncio
from typing import TYPE_CHECKING, Any, Coroutine
import nextcord

from bot.languages import i18n
from bot.databases import GuildDateBases
from bot.misc.utils import to_async
from bot.resources.ether import Emoji


@to_async
class DelCatView(nextcord.ui.View):
    async def __init__(
        self,
        member: nextcord.Member,
        category: nextcord.CategoryChannel
    ) -> None:
        gdb = GuildDateBases(member.guild.id)
        self.locale = await gdb.get('language')

        self.member = member
        self.category = category
        self.embed = nextcord.Embed(
            title=Emoji.warn + " " +
            i18n.t(self.locale, "delcat.issue.title"),
            description=i18n.t(self.locale, "delcat.issue.description",
                               category=self.category.name),
            color=0xED390D
        )
        super().__init__(timeout=10)

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.blurple)
    async def accept(
        self,
        button: nextcord.ui.Button,
        interaction: nextcord.Interaction
    ) -> None:
        tasks = [self.category.delete()] + [channel.delete()
                                            for channel in self.category.channels]
        await asyncio.gather(*tasks)

        embed = nextcord.Embed(
            title=Emoji.success + " " +
            i18n.t(self.locale, "delcat.accept.title",
                   category=self.category.name),
            description=i18n.t(
                self.locale, "delcat.accept.description", count=len(self.category.channels)),
            color=0x57F287
        )

        for channel in self.category.channels:
            asyncio.create_task(channel.delete())
        await self.category.delete()

        await interaction.response.edit_message(embed=embed, view=None)

    @ nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def cancel(
        self,
        button: nextcord.ui.Button,
        interaction: nextcord.Interaction
    ) -> None:
        embed = nextcord.Embed(
            title=Emoji.success + " " +
            i18n.t(self.locale, "delcat.cancel.title"),
            color=0x57F287
        )

        await interaction.response.edit_message(embed=embed, view=None)

    async def interaction_check(
        self,
        interaction: nextcord.Interaction
    ) -> bool:
        return interaction.user == self.member
