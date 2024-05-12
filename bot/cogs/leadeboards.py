import nextcord
import inspect
from nextcord.ext import commands

from typing import List, Tuple, TypeVar

from bot.misc.lordbot import LordBot
from bot.misc.utils import get_award, FissionIterator
from bot.misc.time_transformer import display_time
from bot.views import menus
from bot.databases import GuildDateBases, EconomyMemberDB
from bot.databases import localdb

T = TypeVar("T")
SCORE_STATE_DB = localdb.get_table('score')
MESSAGE_STATE_DB = localdb.get_table('messages')
VOICE_STATE_DB = localdb.get_table('voice_state')


def clear_empty_leaderboard(guild: nextcord.Guild, leaderboard: list):
    for (member_id, balance, bank, total) in leaderboard.copy():
        member = guild._state.get_user(member_id)
        if not member or 0 >= total:
            try:
                leaderboard.remove(
                    (member_id, balance, bank, total))
            except ValueError:
                pass


def get_item_param(item: Tuple[int, T]) -> T:
    return item[1]


def register_key(key: int) -> None:
    def wrapped(func):
        func.__leaderboard_key__ = key
        return func
    return wrapped


class EconomyLeaderboardView(menus.Menus):
    def __init__(self, guild: nextcord.Guild, embed: nextcord.Embed, leaderboards: list, leaderboard_indexs: List[int]):
        self.guild = guild
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings')
        self.currency_emoji = self.economy_settings.get("emoji")
        self.leaderboard_indexs = leaderboard_indexs
        self._embed = embed

        super().__init__(leaderboards, timeout=600)

        self.handler_disable()

        self.remove_item(self.button_previous)
        self.remove_item(self.button_next)

        self.add_item(LeaderboardDropDown(guild.id))

    @property
    def embed(self) -> nextcord.Embed:
        self._embed.clear_fields()
        for (member_id, balance, bank, total) in self.value[self.index]:
            member = self.guild._state.get_user(member_id)
            index = self.leaderboard_indexs.index(member_id)+1
            award = get_award(index)
            self._embed.add_field(
                name=f"{award}. {member.display_name}",
                value=(
                    f"Cash: {balance}{self.currency_emoji} | In bank: {bank}{self.currency_emoji}\n"
                    f"Total balance: {total}{self.currency_emoji}"
                ),
                inline=False
            )

        return self._embed

    async def callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.edit_message(embed=self.embed, view=self)


class LeaderboardDropDown(nextcord.ui.StringSelect):
    def __init__(self, guild_id: int) -> None:
        super().__init__(
            options=[
                nextcord.SelectOption(label="Economy", value="0"),
                nextcord.SelectOption(label="Voice Time", value="1"),
                nextcord.SelectOption(label="Messages", value="2"),
                nextcord.SelectOption(label="Score", value="3")
            ]
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await LeaderboardTypes.set_as_key(int(self.values[0]), interaction.user, interaction.guild, interaction.message)


class AddtionallyViewLeaderboardView(nextcord.ui.View):
    def __init__(self, guild_id: int) -> None:
        super().__init__()
        self.add_item(LeaderboardDropDown(guild_id))


class LeaderboardTypes:
    @staticmethod
    @register_key(0)
    async def set_balance_lb(member: nextcord.Member, guild: nextcord.Guild, message: nextcord.Message):
        gdb = GuildDateBases(guild.id)
        color = gdb.get("color")

        emdb = EconomyMemberDB(guild.id, member.id)
        leaderboard = emdb.get_leaderboards()
        clear_empty_leaderboard(guild, leaderboard)
        fission_leaderboards = FissionIterator(leaderboard, 6).to_list()
        leaderboard_indexs = [member_id for (member_id, *_) in leaderboard]
        user_index = leaderboard_indexs.index(member.id)+1

        file_pedestal = nextcord.File(
            "assets/pedestal.png", filename="pedestal.png")
        embed = nextcord.Embed(
            title="List of leaders by balance",
            description=f"**{member.display_name}**, Your position in the top: **{user_index}**",
            color=color
        )
        embed.set_thumbnail(
            "attachment://pedestal.png")
        embed.set_footer(
            text=guild.name,
            icon_url=guild.icon
        )

        view = EconomyLeaderboardView(
            guild, embed, fission_leaderboards, leaderboard_indexs)

        await message.edit(content="", embed=view.embed, view=view, file=file_pedestal)

    @staticmethod
    @register_key(1)
    async def set_voicetime_lb(member: nextcord.Member, guild: nextcord.Guild, message: nextcord.Message):
        gdb = GuildDateBases(guild.id)
        color = gdb.get("color")
        locale = gdb.get('language')
        leaderboard = sorted(VOICE_STATE_DB.items(),
                             key=get_item_param, reverse=True)
        leaderboard_indexs = [member_id for member_id, _ in leaderboard]

        try:
            user_index = leaderboard_indexs.index(member.id) + 1
        except ValueError:
            user_index = len(leaderboard_indexs) + 1

        file_pedestal = nextcord.File(
            "assets/pedestal.png", filename="pedestal.png")
        embed = nextcord.Embed(
            title="List of leaders by voice time",
            description=f"**{member.display_name}**, Your position in the top: **{user_index}**",
            color=color
        )
        embed.set_thumbnail(
            "attachment://pedestal.png")
        embed.set_footer(
            text=guild.name,
            icon_url=guild.icon
        )

        for index, (member_id, voicetime) in enumerate(leaderboard[:10], start=1):
            member = guild.get_member(member_id)
            embed.add_field(
                name=f"{get_award(index)}. {member.display_name}",
                value=f"Voice time: **{display_time(voicetime, lang=locale, max_items=2)}**",
                inline=False
            )

        await message.edit(content="", embed=embed, view=AddtionallyViewLeaderboardView(guild.id), file=file_pedestal)

    @staticmethod
    @register_key(2)
    async def set_messages_lb(member: nextcord.Member, guild: nextcord.Guild, message: nextcord.Message):
        gdb = GuildDateBases(guild.id)
        color = gdb.get("color")
        locale = gdb.get('language')
        leaderboard = sorted(MESSAGE_STATE_DB.items(),
                             key=get_item_param, reverse=True)
        leaderboard_indexs = [member_id for member_id, _ in leaderboard]

        try:
            user_index = leaderboard_indexs.index(member.id) + 1
        except ValueError:
            user_index = len(leaderboard_indexs) + 1

        file_pedestal = nextcord.File(
            "assets/pedestal.png", filename="pedestal.png")
        embed = nextcord.Embed(
            title="List of leaders by message",
            description=f"**{member.display_name}**, Your position in the top: **{user_index}**",
            color=color
        )
        embed.set_thumbnail(
            "attachment://pedestal.png")
        embed.set_footer(
            text=guild.name,
            icon_url=guild.icon
        )

        for index, (member_id, count_message) in enumerate(leaderboard[:10], start=1):
            member = guild.get_member(member_id)
            embed.add_field(
                name=f"{get_award(index)}. {member.display_name}",
                value=f"Message count: **{count_message}**",
                inline=False
            )

        await message.edit(content="", embed=embed, view=AddtionallyViewLeaderboardView(guild.id),  file=file_pedestal)

    @staticmethod
    @register_key(3)
    async def set_score_lb(member: nextcord.Member, guild: nextcord.Guild, message: nextcord.Message):
        gdb = GuildDateBases(guild.id)
        color = gdb.get("color")
        locale = gdb.get('language')
        leaderboard = sorted(SCORE_STATE_DB.items(),
                             key=get_item_param, reverse=True)
        leaderboard_indexs = [member_id for member_id, _ in leaderboard]

        try:
            user_index = leaderboard_indexs.index(member.id) + 1
        except ValueError:
            user_index = len(leaderboard_indexs) + 1

        file_pedestal = nextcord.File(
            "assets/pedestal.png", filename="pedestal.png")
        embed = nextcord.Embed(
            title="List of leaders by score",
            description=f"**{member.display_name}**, Your position in the top: **{user_index}**",
            color=color
        )
        embed.set_thumbnail(
            "attachment://pedestal.png")
        embed.set_footer(
            text=guild.name,
            icon_url=guild.icon
        )

        for index, (member_id, score) in enumerate(leaderboard[:10], start=1):
            member = guild.get_member(member_id)
            embed.add_field(
                name=f"{get_award(index)}. {member.display_name}",
                value=f"Score: **{score :.0f}**",
                inline=False
            )

        await message.edit(content="", embed=embed, view=AddtionallyViewLeaderboardView(guild.id),  file=file_pedestal)

    @classmethod
    async def set_as_key(cls, key: int, member: nextcord.Member, guild: nextcord.Guild, message: nextcord.Message):
        for _, item in inspect.getmembers(cls):
            if not (hasattr(item, "__leaderboard_key__")
                    and item.__leaderboard_key__ == key):
                continue
            await item(member, guild, message)


class Leaderboards(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

    @commands.command(name="leaderboard", aliases=["lb", "leaders", "top"])
    async def leaderboard(self, ctx: commands.Context):
        message = await ctx.send("Uploading data...")
        await LeaderboardTypes.set_score_lb(ctx.author, ctx.guild, message)


def setup(bot):
    bot.add_cog(Leaderboards(bot))
