import logging
import nextcord

from bot.databases import localdb
from bot.databases.handlers.guildHD import GuildDateBases


_log = logging.getLogger(__name__)


class TempVoiceModule:
    def __init__(self, guild: nextcord.Guild) -> None:
        ...

    @classmethod
    async def disconnect_voice(cls, member: nextcord.Member, channel: nextcord.VoiceChannel) -> None:
        _log.trace('%s connected voice %s', member, channel)

    @classmethod
    async def connect_voice(cls, member: nextcord.Member, channel: nextcord.VoiceChannel) -> None:
        _log.trace('%s disconnected voice %s', member, channel)
