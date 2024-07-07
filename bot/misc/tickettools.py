import asyncio
import nextcord
from bot.misc import utils
from typing import Optional

from bot.views import tickets


class ModuleTicket:
    ticket_channel = None
    __closed = False
    __deleted = False

    def __init__(
        self,
        guild: nextcord.Guild,
        category: nextcord.CategoryChannel,
        ticket_data: Optional[dict] = None
    ) -> None:
        self.guild = guild
        self.category = category
        self.ticket_data = ticket_data

        self.loop = guild._state.loop

    async def create(self, member: nextcord.Member):
        self.ticket_channel = await self.guild.create_text_channel(
            name=f"ticket-{member.name}",
            reason="Create ticket",
            category=self.category
        )

        content = utils.lord_format("{  member.mention  } Опиши свою проблему!",
                                    {"member.mention": member.mention})
        view = tickets.CloseTicketView(self)
        await self.ticket_channel.send(content, view=view)

    async def close(self):
        view = tickets.DelopTicketView(self)
        await self.ticket_channel.send("Тикет закрыт!", view=view)
        self.__closed = True

    async def delete(self):
        if self.__closed is False:
            return

        await self.ticket_channel.send("Тикет будет удален через несколько секунд!")
        self.__deleted = self.loop.call_later(
            5, self.loop.create_task, self.ticket_channel.delete(reason="Delete ticket"))

    async def reopen(self):
        if self.__closed is False and self.__deleted is False:
            return
        if th := self.__deleted:
            th._args[0].close()
            th.cancel()

        self.__closed = False
        self.__deleted = False

        await self.ticket_channel.send("Тикет снова открыт!")
