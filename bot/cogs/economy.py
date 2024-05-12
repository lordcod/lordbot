
import nextcord
from nextcord.ext import commands

from bot.databases import EconomyMemberDB, GuildDateBases
from bot.misc import logstool
from bot.misc.lordbot import LordBot
from bot.resources.errors import NotActivateEconomy
from bot.resources.ether import Emoji
from nextcord.utils import escape_markdown

import time
from typing import Optional, Union, Literal

from bot.views.economy_shop import EconomyShopView

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
            raise NotActivateEconomy("Economy is disabled on the server")
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
            await logstool.Logs(ctx.guild).add_currency(ctx.author, award, reason=f'{ctx.command.name} reward')
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
                      member: Optional[nextcord.Member] = None):
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

    @commands.command()
    async def shop(self, ctx: commands.Context):
        view = EconomyShopView(ctx.guild)
        await ctx.send(embed=view.embed, view=view)

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
        elif sum > from_account.get('balance', 0):
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}bal`")
            return

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You were given **{sum}**{currency_emoji}"
        )
        embed.set_footer(
            text=f'From {ctx.author.display_name}', icon_url=ctx.author.display_avatar)

        from_account["balance"] -= sum
        to_account["balance"] += sum
        await logstool.Logs(ctx.guild).add_currency(member, sum, reason=f'received from a {ctx.author.name} member')
        await logstool.Logs(ctx.guild).remove_currency(ctx.author, sum, reason=f'passed to the {member.name} participant')

        await ctx.send(embed=embed)

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

        account['balance'] -= sum
        account['bank'] += sum

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

        await ctx.send(f"You have transferred the amount of **{sum}**{currency_emoji} to {member.display_name}")
        await ctx.send(f"You passed {member.display_name}, **{sum}**{currency_emoji}")
        await logstool.Logs(ctx.guild).add_currency(member, sum, moderator=ctx.author)

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

        if account.get('balance') >= sum:
            await ctx.send('The operation cannot be performed because the balance will become negative during it')
            return

        account["balance"] -= sum

        await ctx.send(f"You have withdrawn an amount of **{sum}**{currency_emoji} from {member.display_name}")
        await ctx.send(f"You passed `{member.display_name}`, **{sum}**{currency_emoji} ")
        await logstool.Logs(ctx.guild).remove_currency(member, sum, moderator=ctx.author)


def setup(bot):
    bot.add_cog(Economy(bot))
