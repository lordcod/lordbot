import nextcord
from typing import List
from databases import localdb

GIVEAWAY_DB = localdb.get_table('giveaway')


data = {
    "guild_id": 1179069504186232852,
    "sponser_id": 636824998123798531,
    "prize": "LordCord Pro",
    "quantity": 1,
    "date_end": 1710606949,
    "types": []
}


class GiveawayTypesChecker:
    def __init__(self, types: List[int]) -> None:
        self.types = types

    def check_count_invites(): ...

    def check_date_join(): ...

    def check_min_balance(): ...

    def check_guild_connect(): ...

    def check_voice_connect(): ...

    def check_voice_connect_latest(): ...

    def check_min_voice_time(): ...

    def check_min_voice_time_gap(): ...

    def check_min_level(): ...

    types_function = {
        0: check_count_invites,
        1: check_date_join,
        2: check_min_balance,
        3: check_guild_connect,
        4: check_voice_connect,
        5: check_voice_connect_latest,
        6: check_min_voice_time,
        7: check_min_voice_time_gap,
        8: check_min_level
    }


class Giveaway:
    def __init__(
        self,
        guild: nextcord.Guild,
        message_id: int
    ) -> None:
        self.guild = guild
        self.message_id = message_id

    @classmethod
    async def create(
        cls,
        guild: nextcord.Guild,
        channel: nextcord.TextChannel,
        sponser: nextcord.Member,
        prize: str,
        description: str,
        quantity: int,
        date_end: int,
        types: List[int]
    ) -> 'Giveaway':
        giveaway_data = {
            "guild_id": guild.id,
            "sponser_id": sponser.id,
            "prize": prize,
            "description": description,
            "quantity": quantity,
            "date_end": date_end,
            "types": types,
            "winners": None
        }

        message = await channel.send()

    @staticmethod
    def get_embed(giveaway_data: dict) -> nextcord.Embed:
        embed = nextcord.Embed(
            title=giveaway_data.get("prize"),
            description=giveaway_data.get("description")
        )
        embed.
