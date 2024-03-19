import asyncio
import nextcord
import random
from typing import List
from bot.databases import localdb
from bot.views import giveaway as views_giveaway

GIVEAWAY_DB = localdb.get_table('giveaway')


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
            "completed": False,
            "winners": None
        }

        embed = cls.get_embed(giveaway_data)

        message = await channel.send(embed=embed, view=views_giveaway.GiveawayView())

        GIVEAWAY_DB[message.id] = giveaway_data

        return cls(guild, message.id)

    async def complete(self) -> None:
        self.update_giveaway_data()

        winner_ids = random.choices(
            self.giveaway_data['entries_ids'], k=self.giveaway_data['quantity'])
        winners = map(self.guild.get_member,
                      winner_ids)

        self.giveaway_data['winners'] = winner_ids
        self.giveaway_data['completed'] = True
        GIVEAWAY_DB[self.message_id] = self.giveaway_data

        channel = self.guild.get_channel(self.giveaway_data.get('channel_id'))

        asyncio.create_task(self.update_message())
        asyncio.create_task(channel.send(
            f"Congratulations {', '.join([wu.mention for wu in winners])}! You won the LordCord Premium!"))

    def update_giveaway_data(self) -> None:
        self.giveaway_data = GIVEAWAY_DB[self.message_id]

    async def update_message(self) -> None:
        channel = self.guild.get_channel(self.giveaway_data.get('channel_id'))
        message = channel.get_partial_message(self.message_id)
        embed = self.get_completed_embed() if self.giveaway_data.get(
            'completed') else self.get_embed(self.giveaway_data)
        view = None if self.giveaway_data.get(
            'completed') else views_giveaway.GiveawayView()

        await message.edit(embed=embed, view=view)

    @staticmethod
    def get_embed(giveaway_data) -> nextcord.Embed:
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

    def get_completed_embed(self) -> nextcord.Embed:
        winners = map(self.guild.get_member,
                      self.giveaway_data.get('winners'))

        embed = nextcord.Embed(
            title=self.giveaway_data.get("prize"),
            description=self.giveaway_data.get("description")
        )

        embed.add_field(
            name='',
            value=(
                f"Ends: <t:{self.giveaway_data.get('date_end') :.0f}:f> (<t:{self.giveaway_data.get('date_end') :.0f}:R>)\n"
                f"Sponsored by <@{self.giveaway_data.get('sponser_id')}>\n"
                f"Entries: **{len(self.giveaway_data.get('entries_ids'))}**\n"
                f"Winners: **{', '.join([wu.mention for wu in winners])}**"
            )
        )

        return embed

    def check_participation(self, member_id: int) -> bool:
        return member_id in self.giveaway_data.get('entries_ids')

    def promote_participant(self, member_id: int) -> None:
        self.giveaway_data.get('entries_ids').append(member_id)

    def demote_participant(self, member_id: int) -> None:
        self.giveaway_data.get('entries_ids').remove(member_id)
