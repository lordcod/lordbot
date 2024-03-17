import nextcord
from typing import List
from bot.databases import localdb
from bot.views import giveaway as views_giveaway

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
        if message_id not in GIVEAWAY_DB:
            raise TypeError

        self.guild = guild
        self.message_id = message_id
        self.giveaway_data: dict = GIVEAWAY_DB.get(message_id)

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
            "channel_id": channel.id,
            "sponser_id": sponser.id,
            "prize": prize,
            "description": description,
            "quantity": quantity,
            "date_end": date_end,
            "types": types,
            "entries_ids": [],
            "winners": None
        }

        embed = cls.get_embed(giveaway_data)

        message = await channel.send(embed=embed, view=views_giveaway.GiveawayView())

        GIVEAWAY_DB[message.id] = giveaway_data

        return cls(guild, message.id)

    async def update_message(self) -> None:
        channel = self.guild.get_channel(self.giveaway_data.get('channel_id'))
        message = channel.get_partial_message(self.message_id)
        embed = self.get_embed(self.giveaway_data)

        await message.edit(embed=embed, view=views_giveaway.GiveawayView())

    @staticmethod
    def get_embed(giveaway_data: dict) -> nextcord.Embed:
        embed = nextcord.Embed(
            title=giveaway_data.get("prize"),
            description=giveaway_data.get("description")
        )

        embed.add_field(
            name='',
            value=(
                f"Ends: <t:{giveaway_data.get('date_end') :.0f}:f> (<t:{giveaway_data.get('date_end') :.0f}:R>)\n"
                f"Sponsored by <@{giveaway_data.get('sponser_id')}>\n"
                f"Entries: **{len(giveaway_data.get('entries_ids'))}**\n"
                f"Winners: **{giveaway_data.get('quantity')}**"
            )
        )

        return embed

    def check_participation(self, member_id: int) -> bool:
        return member_id in self.giveaway_data.get('entries_ids')

    def promote_participant(self, member_id: int) -> None:
        self.giveaway_data.get('entries_ids').append(member_id)

    def demote_participant(self, member_id: int) -> None:
        self.giveaway_data.get('entries_ids').remove(member_id)
