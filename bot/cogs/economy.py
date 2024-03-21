import nextcord
from nextcord.ext import commands

from bot.databases import EconomyMemberDB, GuildDateBases
from bot.misc.lordbot import LordBot
from bot.resources.errors import NotActivateEconomy
from bot.resources.ether import Emoji
from bot.misc.utils import get_award
from nextcord.utils import escape_markdown

import time
from typing import Optional, Union, Literal

timeout_rewards = {"daily": 86400, "weekly": 604800, "monthly": 2592000}


class Economy(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

        super().__init__()

    def cog_check(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        es = gdb.get('economic_settings')
        operate = es.get('operate', False)
        if not operate:
            raise NotActivateEconomy("Economy is not enabled on the server")
        return True

    async def handler_rewards(self, ctx: commands.Context):
        loctime = time.time()
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        award = eco_sets.get(ctx.command.name, 0)
        if award <= 0:
            await ctx.send("Unfortunately this reward is not available if you are the server administrator change the reward")
            return
        if loctime > account.get(ctx.command.name, 0):
            wait_long = loctime+timeout_rewards.get(ctx.command.name)

            embed = nextcord.Embed(
                title="You have received a gift",
                description=f"In size {award}{currency_emoji} come through <t:{wait_long :.0f}:R>",
                color=color
            )
            account[ctx.command.name] = wait_long
            account['balance'] += award
        else:
            embed = nextcord.Embed(
                title="The reward is not available",
                description=f'Try again after <t:{account.get(ctx.command.name) :.0f}:R>',
                color=color
            )
        await ctx.send(embed=embed)

    @commands.command(name='daily')
    async def daily(self, ctx: commands.Context):
        await self.handler_rewards(ctx)

    @commands.command(name='weekly')
    async def weekly(self, ctx: commands.Context):
        await self.handler_rewards(ctx)

    @commands.command(name='monthly')
    async def monthly(self, ctx: commands.Context):
        await self.handler_rewards(ctx)

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self,
                      ctx: commands.Context,
                      member: nextcord.Member = None):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        prefix = escape_markdown(gdb.get('prefix'))
        color = gdb.get('color')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')

        account = EconomyMemberDB(ctx.guild.id, member.id)
        balance = account.get('balance', 0)
        bank = account.get('bank', 0)
        loctime = time.time()

        description = ""
        if account.get('daily', 0) < loctime:
            description += f"— Daily Bonus ({prefix}daily)\n"
        if account.get('weekly', 0) < loctime:
            description += f"— Weekly Bonus ({prefix}weekly)\n"
        if account.get('monthly', 0) < loctime:
            description += f"— Monthly Bonus ({prefix}monthly)\n"
        if description:
            description = f"{Emoji.award} Available Rewards:\n{description}"

        embed = nextcord.Embed(
            title="Balance",
            color=color,
            description=description
        )
        embed.set_author(name=member.display_name,
                         icon_url=member.display_avatar)

        embed.add_field(
            name=f"{Emoji.money} Cash:",
            value=f'{balance}{currency_emoji}',
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bank} In bank:",
            value=f'{bank}{currency_emoji}',
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bagmoney} Total balance:",
            value=f'{balance+bank}{currency_emoji}',
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="leaderboard", aliases=["lb", "leaders", "top"])
    async def leaderboard(self, ctx: commands.Context):
        message = await ctx.send("Uploading data...")

        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get("color")
        economy_settings: dict = gdb.get('economic_settings')
        currency_emoji = economy_settings.get("emoji")

        emdb = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        leaderboard = emdb.get_leaderboards()

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

        for (member_id, balance, bank, total) in leaderboard[0:10]:
            member = ctx.guild.get_member(member_id)
            if not member or 0 >= total:
                leaderboard_indexs.remove(member_id)
                continue

            index = leaderboard_indexs.index(member_id)+1
            award = get_award(index)

            embed.add_field(
                name=f"{award}. {member.display_name}",
                value=(
                    f"Cash: {balance}{currency_emoji} | In bank: {bank}{currency_emoji}\n"
                    f"Total balance: {total}{currency_emoji}"
                ),
                inline=False
            )
        await message.delete()
        await ctx.send(embed=embed, file=file_pedestal)

    @commands.command(name="pay")
    async def pay(self, ctx: commands.Context, member: nextcord.Member, sum: int):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        prefix = gdb.get('prefix')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        from_account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        to_account = EconomyMemberDB(ctx.guild.id, member.id)

        if sum <= 0:
            await ctx.send(content="Specify the amount more **0**")
            return
        elif (from_account.get('balance', 0)-sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}bal`")
            return

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You were given **{sum}**{currency_emoji}"
        )
        embed.set_footer(
            text=f'From {ctx.author.display_name}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

        from_account["balance"] -= sum
        to_account["balance"] += sum

    @commands.command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx: commands.Context, sum: Union[Literal['all'], int]):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        prefix = gdb.get('prefix')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        balance = account.get('balance', 0)

        if sum == "all":
            sum = balance

        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if (balance - sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            return
        account['balance'] = account['balance'] - sum
        account['bank'] = account['bank'] + sum

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You have transferred **{sum}**{currency_emoji} to the bank account"
        )
        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="withdraw", aliases=["wd"])
    async def withdraw(self, ctx: commands.Context, sum: Union[Literal['all'], int]):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        prefix = gdb.get('prefix')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        bank = account.get('bank', 0)

        if sum == "all":
            sum = bank

        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if (bank - sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            return
        account['balance'] += sum
        account['bank'] -= sum

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You have transferred **{sum}**{currency_emoji} to the account"
        )
        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="gift")
    @commands.has_permissions(administrator=True)
    async def gift(self, ctx: commands.Context, member: Optional[nextcord.Member], sum: int):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, member.id)

        if sum > 1_000_000:
            await ctx.send(f"The maximum amount for this server - {1_000_000 :,}{currency_emoji}")
            return
        if 0 >= sum:
            await ctx.send("The amount must be positive")
            return

        account["balance"] += sum

        await ctx.send(f"You passed {member.display_name}, **{sum}**{currency_emoji}")

    @commands.command(name="take")
    @commands.has_permissions(administrator=True)
    async def take(self, ctx: commands.Context, member: Optional[nextcord.Member], sum: int):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, member.id)

        if sum > 1_000_000:
            await ctx.send(f"The maximum amount for this server - {1_000_000 :,}{currency_emoji}")
            return
        if 0 >= sum:
            await ctx.send("The amount must be positive")
            return

        if 0 > (account.get('balance')-sum):
            await ctx.send('The operation cannot be performed because the balance will become negative during it')
            return

        account["balance"] -= sum

        await ctx.send(f"You passed `{member.display_name}`, **{sum}**{currency_emoji} ")


def setup(bot):
    bot.add_cog(Economy(bot))
