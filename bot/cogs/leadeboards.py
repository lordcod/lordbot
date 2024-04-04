import nextcord
from nextcord.ext import commands

from typing import List

from bot.misc.lordbot import LordBot
from bot.misc.utils import get_award, FissionIterator
from bot.views import menus
from bot.databases import GuildDateBases, EconomyMemberDB


class EconomyLeaderboardView(menus.Main):
    def __init__(self, guild: nextcord.Guild, embed: nextcord.Embed, leaderboards: list, leaderboard_indexs: List[int]):
        self.guild = guild
        self.gdb = GuildDateBases(guild.id)
        self.economy_settings = self.gdb.get('economic_settings')
        self.currency_emoji = self.economy_settings.get("emoji")
        self.leaderboard_indexs = leaderboard_indexs
        self._embed = embed

        super().__init__(leaderboards)

        self.handler_disable()

        self.remove_item(self.button_previous)
        self.remove_item(self.button_next)

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


def clear_empty_leaderboard(guild: nextcord.Guild, leaderboard: list):
    for (member_id, balance, bank, total) in leaderboard.copy():
        member = guild._state.get_user(member_id)
        if not member or 0 >= total:
            try:
                leaderboard.remove(
                    (member_id, balance, bank, total))
            except ValueError:
                pass


class Leaderboards(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

    @commands.command(name="leaderboard", aliases=["lb", "leaders", "top"])
    async def leaderboard(self, ctx: commands.Context):
        message = await ctx.send("Uploading data...")

        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get("color")

        emdb = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        leaderboard = emdb.get_leaderboards()
        clear_empty_leaderboard(ctx.guild, leaderboard)
        fission_leaderboards = FissionIterator(leaderboard, 6).to_list()
        leaderboard_indexs = [member_id for (member_id, *_) in leaderboard]
        user_index = leaderboard_indexs.index(ctx.author.id)+1

        file_pedestal = nextcord.File(
            "assets/pedestal.png", filename="pedestal.png")
        embed = nextcord.Embed(
            title="List of leaders by balance",
            description=f"**{ctx.author.display_name}**, Your position in the top: **{user_index}**",
            color=color
        )
        embed.set_thumbnail(
            "attachment://pedestal.png")
        embed.set_footer(
            text=ctx.guild.name,
            icon_url=ctx.guild.icon
        )

        view = EconomyLeaderboardView(
            ctx.guild, embed, fission_leaderboards, leaderboard_indexs)

        await message.edit(content=None, embed=view.embed, view=view, file=file_pedestal)


def setup(bot):
    bot.add_cog(Leaderboards(bot))
