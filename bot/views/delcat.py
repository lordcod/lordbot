import asyncio
from typing import Any, Coroutine
import nextcord
import asyncio

from bot.languages import i18n
from bot.databases import GuildDateBases
from bot.resources.ether import Emoji


class DelCatView(nextcord.ui.View):
    def __init__(
        self,
        member: nextcord.Member,
        category: nextcord.CategoryChannel
    ) -> None:
        gdb = GuildDateBases(member.guild.id)
        self.locale = gdb.get('language')

        self.member = member
        self.category = category
        self.embed = nextcord.Embed(
            title=Emoji.warn + " " +
            i18n.t(self.locale, "delcat.issue.title"),
            description=i18n.t(self.locale, "delcat.issue.description",
                               category=self.category.name),
            color=0xED390D
        )
        super().__init__()

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

        await interaction.message.edit(embed=embed, view=None)

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

        await interaction.message.edit(embed=embed, view=None)

    async def interaction_check(
        self,
        interaction: nextcord.Interaction
    ) -> Coroutine[Any, Any, bool]:
        return interaction.user == self.member
