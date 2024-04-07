import asyncio
import nextcord
from typing import List, Coroutine, Any
from bot.databases import localdb
from bot.databases.varstructs import GiveawayData
from bot.databases import GuildDateBases
from bot.misc import utils
from bot.views import giveaway as views_giveaway


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


class GiveawayConfig:
    prize: str = None
    sponsor: nextcord.Member = None
    channel: nextcord.TextChannel = None
    description: str = None
    quantity: int = 1
    date_end: int | float = None


class Giveaway:
    giveaway_data: GiveawayData

    def __init__(
        self,
        guild: nextcord.Guild,
        message_id: int
    ) -> None:
        gdb = GuildDateBases(guild.id)
        giveaways = gdb.get('giveaways')

        if message_id not in giveaways:
            raise TypeError

        self.guild = guild
        self.message_id = message_id
        self.giveaway_data = giveaways.get(message_id)

    @classmethod
    def set_lord_timer_handler(cls, lord_handler_timer):
        cls.lord_handler_timer = lord_handler_timer

    @classmethod
    async def create(
        cls,
        guild: nextcord.Guild,
        channel: nextcord.TextChannel,
        sponser: nextcord.Member,
        prize: str,
        description: str,
        quantity: int,
        date_end: int
    ) -> 'Giveaway':
        gdb = GuildDateBases(guild.id)
        giveaways = gdb.get('giveaways')
        key, token = utils.generate_random_token()

        giveaway_data = {
            "guild_id": guild.id,
            "channel_id": channel.id,
            "sponsor_id": sponser.id,
            "prize": prize,
            "description": description,
            "quantity": quantity,
            "date_end": date_end,
            "types": [],
            "entries_ids": [],
            "completed": False,
            "winners": None,
            "key": key,
            "token": token
        }

        embed = cls.get_embed(giveaway_data)

        message = await channel.send(embed=embed, view=views_giveaway.GiveawayView())

        giveaways[message.id] = giveaway_data

        gdb.set('giveaways', giveaways)

        return cls(guild, message.id)

    @classmethod
    def create_as_config(
        cls,
        guild: nextcord.Guild,
        giveaway_config: GiveawayConfig
    ) -> Coroutine[Any, Any, 'Giveaway']:
        return cls.create(
            guild=guild,
            channel=giveaway_config.channel,
            sponser=giveaway_config.sponsor,
            prize=giveaway_config.prize,
            description=giveaway_config.description,
            quantity=giveaway_config.quantity,
            date_end=giveaway_config.date_end
        )

    async def complete(self) -> None:
        gdb = GuildDateBases(self.guild.id)
        giveaways = gdb.get('giveaways')

        winner_number = utils.decrypt_token(
            self.giveaway_data.get('key'), self.giveaway_data.get('token'))
        winner_ids = []
        entries_ids = self.giveaway_data.get('entries_ids').copy()

        for _ in range(self.giveaway_data.get('quantity')):
            win = entries_ids.pop(winner_number % len(entries_ids))
            winner_ids.append(win)

        winners = map(self.guild.get_member,
                      winner_ids)

        self.giveaway_data['winners'] = winner_ids
        self.giveaway_data['completed'] = True
        giveaways[self.message_id] = self.giveaway_data
        gdb.set('giveaways', giveaways)

        channel = self.guild.get_channel(self.giveaway_data.get('channel_id'))

        asyncio.create_task(self.update_message())
        asyncio.create_task(channel.send(
            f"Congratulations {', '.join([wu.mention for wu in winners])}! You won the {self.giveaway_data['prize']}!"))

    async def update_message(self) -> None:
        channel = self.guild.get_channel(self.giveaway_data.get('channel_id'))
        message = channel.get_partial_message(self.message_id)
        embed = self.get_completed_embed() if self.giveaway_data.get(
            'completed') else self.get_embed(self.giveaway_data)
        view = views_giveaway.GiveawayView(
        ) if not self.giveaway_data.get('completed') else None

        await message.edit(embed=embed, view=view)

    @staticmethod
    def get_embed(giveaway_data: dict) -> nextcord.Embed:
        giveaway_description = giveaway_data.get(
            'description')+'\n\n' if giveaway_data.get('description') else ''
        embed = nextcord.Embed(
            title=giveaway_data.get("prize"),
            description=(
                f"{giveaway_description}"
                f"Ends: <t:{giveaway_data.get('date_end') :.0f}:f> (<t:{giveaway_data.get('date_end') :.0f}:R>)\n"
                f"Sponsored by <@{giveaway_data.get('sponsor_id')}>\n"
                f"Entries: **{len(giveaway_data.get('entries_ids'))}**\n"
                f"Winners: **{giveaway_data.get('quantity')}**"
            )
        )
        embed.set_footer(
            text=f"Key: {giveaway_data.get('key')}"
        )

        return embed

    def get_completed_embed(self) -> nextcord.Embed:
        winners = filter(lambda item: item is not None,
                         map(self.guild.get_member,
                             self.giveaway_data.get('winners')))
        giveaway_description = self.giveaway_data.get(
            'description')+'\n\n' if self.giveaway_data.get('description') else ''
        embed = nextcord.Embed(
            title=self.giveaway_data.get("prize"),
            description=(
                f"{giveaway_description}"
                f"Ends: <t:{self.giveaway_data.get('date_end') :.0f}:f> (<t:{self.giveaway_data.get('date_end') :.0f}:R>)\n"
                f"Sponsored by <@{self.giveaway_data.get('sponsor_id')}>\n"
                f"Entries: **{len(self.giveaway_data.get('entries_ids'))}**\n"
                f"Winners: **{', '.join([wu.mention for wu in winners])}**"
            )
        )

        return embed

    def check_participation(self, member_id: int) -> bool:
        return member_id in self.giveaway_data.get('entries_ids')

    def promote_participant(self, member_id: int) -> None:
        gdb = GuildDateBases(self.guild.id)
        giveaways = gdb.get('giveaways')
        self.giveaway_data.get('entries_ids').append(member_id)
        giveaways[self.message_id] = self.giveaway_data

    def demote_participant(self, member_id: int) -> None:
        gdb = GuildDateBases(self.guild.id)
        giveaways = gdb.get('giveaways')
        self.giveaway_data.get('entries_ids').remove(member_id)
        giveaways[self.message_id] = self.giveaway_data
