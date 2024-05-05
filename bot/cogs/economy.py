
import random
import asyncio
import random
import nextcord
from nextcord.ext import commands


import time
from typing import Callable, Dict, List, Optional, Tuple, TypedDict, Union, Literal
from nextcord.utils import escape_markdown

import time
import orjson
from typing import Optional, Union, Literal


from bot.databases import EconomyMemberDB, GuildDateBases
from bot.views.economy_shop import EconomyShopView
from bot.misc.lordbot import LordBot
from bot.resources.errors import NotActivateEconomy
from bot.resources.ether import Emoji
from bot.misc.utils import BlackjackGame, get_award
from nextcord.utils import escape_markdown


from bot.views.blackjack import BlackjackView


class ArgumntRouletteItem(TypedDict):
    input_data_condition: Callable[[str], bool]
    random_condition: Callable[[str, int], bool]
    multiplier: int


timeout_rewards: Dict[str, int] = {
    "daily": 86400, "weekly": 604800, "monthly": 2592000}
roulette_games: Dict[int,
                     Tuple[
                         Callable[[], None],
                         List[Tuple[nextcord.Member, int, str]],
                         nextcord.Message]
                     ] = {}
arguments_roulette: List[ArgumntRouletteItem] = [
    {
        "input_data_condition": lambda val: val.isdigit() and 0 <= int(val) <= 36,
        "random_condition": lambda val, ran: ran == int(val),
        "multiplier": 35,
    },
    {
        "input_data_condition": lambda val: val == "1 to 12" or val.replace(" ", "") == "1-12",
        "random_condition": lambda val, ran: 1 <= ran <= 12,
        "multiplier": 3,
    },
    {
        "input_data_condition": lambda val: val == "13 to 24" or val.replace(" ", "") == "13-24",
        "random_condition": lambda val, ran: 13 <= ran <= 24,
        "multiplier": 3,
    },
    {
        "input_data_condition": lambda val: val == "25 to 36" or val.replace(" ", "") == "25-36",
        "random_condition": lambda val, ran: 25 <= ran <= 36,
        "multiplier": 3,
    },
    {
        "input_data_condition": lambda val: val == "1 to 18" or val.replace(" ", "") == "1-18",
        "random_condition": lambda val, ran: 1 <= ran <= 18,
        "multiplier": 2,
    },
    {
        "input_data_condition": lambda val: val == "19 to 36" or val.replace(" ", "") == "19-36",
        "random_condition": lambda val, ran: 19 <= ran <= 36,
        "multiplier": 2,
    },
    {
        "input_data_condition": lambda val: val == "red",
        "random_condition": lambda val, ran: ran in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
        "multiplier": 2,
    },
    {
        "input_data_condition": lambda val: val == "black",
        "random_condition": lambda val, ran: ran in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
        "multiplier": 2,
    },
    {
        "input_data_condition": lambda val: val == "even",
        "random_condition": lambda val, ran: ran % 2 == 0,
        "multiplier": 2,
    },
    {
        "input_data_condition": lambda val: val == "odd",
        "random_condition": lambda val, ran: ran % 2 == 1,
        "multiplier": 2,
    },
    {
        "input_data_condition": lambda val: val == "1st",
        "random_condition": lambda val, ran: ran in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
        "multiplier": 3,
    },
    {
        "input_data_condition": lambda val: val == "2nd",
        "random_condition": lambda val, ran: ran in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        "multiplier": 3,
    },
    {
        "input_data_condition": lambda val: val == "3rd",
        "random_condition": lambda val, ran: ran in [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        "multiplier": 3
    },
]


def create_roulette_task():
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    _task = loop.call_later(10, future.set_result, None)

    def wrapped():
        nonlocal _task
        _task.cancel()
        _task = loop.call_later(10, future.set_result, None)
    return future, wrapped


def is_valid_roulette_argument(val: str) -> bool:
    return any(data['input_data_condition'](val) for data in arguments_roulette)


with open("bot/languages/works.json", "rb") as file:
    list_of_works = orjson.loads(file.read())

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

    async def handle_rewards(self, ctx: commands.Context):
        loctime = time.time()
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        award = economic_settings.get(ctx.command.name, 0)
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
        await self.handle_rewards(ctx)

    @commands.command(name='weekly')
    async def weekly(self, ctx: commands.Context):
        await self.handle_rewards(ctx)

    @commands.command(name='monthly')
    async def monthly(self, ctx: commands.Context):
        await self.handle_rewards(ctx)

    @commands.command(name='work')
    async def work(self, ctx: commands.Context):
        loctime = time.time()
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        gdb = GuildDateBases(ctx.guild.id)
        locale = gdb.get('language')
        color = gdb.get('color')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        work_info = eco_sets.get('work')

        if loctime > account.get('work', 0)+work_info['cooldown']:
            amount = random.randint(work_info['min'], work_info['max'])

            embed = nextcord.Embed(
                title="Time to work",
                description=random.choice(
                    list_of_works.get(locale, list_of_works['en'])).format(amount=amount, emoji=currency_emoji),
                color=color
            )
            embed.add_field(
                name="",
                value=f"Come to work through <t:{loctime+work_info['cooldown'] :.0f}:R>"
            )
            account['work'] = loctime
            account['balance'] += amount
        else:
            embed = nextcord.Embed(
                title="It's too early to work",
                description=f"Try again after <t:{account.get(ctx.command.name)+work_info['cooldown'] :.0f}:R>",
                color=color
            )
        await ctx.send(embed=embed)

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self,
                      ctx: commands.Context,
                      member: Optional[nextcord.Member] = None):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        prefix = escape_markdown(gdb.get('prefix'))
        color = gdb.get('color')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')

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
    async def pay(self, ctx: commands.Context, member: nextcord.Member, amount: int):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        prefix = gdb.get('prefix')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        from_account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        to_account = EconomyMemberDB(ctx.guild.id, member.id)

        if amount <= 0:
            await ctx.send(content="Specify the amount more **0**")
            return
        elif amount > from_account.get('balance', 0):
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}bal`")
            return

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You were given **{amount}**{currency_emoji}"
        )
        embed.set_footer(
            text=f'From {ctx.author.display_name}', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

        from_account["balance"] -= amount
        to_account["balance"] += amount

        await ctx.send(embed=embed)

    @commands.command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx: commands.Context, amount: Union[Literal['all'], int]):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        prefix = gdb.get('prefix')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        balance = account.get('balance', 0)

        if amount == "all":
            amount = balance

        if amount <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if (balance - amount) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            return
        account['balance'] -= amount
        account['bank'] += amount

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You have transferred **{amount}**{currency_emoji} to the bank account"
        )
        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="withdraw", aliases=["wd"])
    async def withdraw(self, ctx: commands.Context, amount: Union[Literal['all'], int]):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        prefix = gdb.get('prefix')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        bank = account.get('bank', 0)

        if amount == "all":
            amount = bank

        if amount <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if (bank - amount) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            return
        account['balance'] += amount
        account['bank'] -= amount

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You have transferred **{amount}**{currency_emoji} to the account"
        )
        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="gift")
    @commands.has_permissions(administrator=True)
    async def gift(self, ctx: commands.Context, member: Optional[nextcord.Member], amount: int):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, member.id)

        if amount > 1_000_000:
            await ctx.send(f"The maximum amount for this server - {1_000_000: ,}{currency_emoji}")
            return
        if 0 >= amount:
            await ctx.send("The amount must be positive")
            return

        account["balance"] += amount

        await ctx.send(f"You passed {member.display_name}, **{amount}**{currency_emoji}")

    @commands.command(name="take")
    @commands.has_permissions(administrator=True)
    async def take(self, ctx: commands.Context, member: Optional[nextcord.Member], amount: int):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, member.id)

        if amount > 1_000_000:
            await ctx.send(f"The maximum amount for this server - {1_000_000: ,}{currency_emoji}")
            return
        if 0 >= amount:
            await ctx.send("The amount must be positive")
            return

        if 0 > (account.get('balance')-amount):
            await ctx.send('The operation cannot be performed because the balance will become negative during it')
            return

        account["balance"] -= amount

        await ctx.send(f"You passed `{member.display_name}`, **{amount}**{currency_emoji} ")

    @commands.command(name="roulette", aliases=["rou"])
    async def roulette(self, ctx: commands.Context, amount: int, *, val: str):
        gdb = GuildDateBases(ctx.guild.id)
        prefix = gdb.get('prefix')
        color = gdb.get('color')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        val = val.lower()

        if not is_valid_roulette_argument(val):
            await ctx.send(content=f"An incorrect value has been entered for the roulette game, use the command `{prefix}help {ctx.command.name}` to find out the arguments")
            raise TypeError('Planned error')
        if amount <= 0:
            await ctx.send(content="Specify the amount more `0`")
            raise TypeError('Planned error')
        if amount > account['balance']:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            raise TypeError('Planned error')

        account["balance"] -= amount

        if rg := roulette_games.get(ctx.guild.id):
            postpone, listener, mes = rg
            postpone()
            listener.append((ctx.author, amount, val))
            embed = nextcord.Embed(
                title="New roulette game started!",
                description='\n'.join(
                    [f"{member.mention} have placed a bet of {amount}{currency_emoji} on {val}" for member, amount, val in listener]),
                color=color
            )
            embed.set_author(name=ctx.guild.name,
                             icon_url=ctx.guild.icon)
            embed.set_footer(
                text="Time remaining: 10 seconds after each bet (maximum 1 minute)")
            asyncio.create_task(mes.edit(embed=embed))
            if ctx.channel == mes.channel:
                asyncio.create_task(ctx.message.add_reaction(Emoji.success))
            else:
                asyncio.create_task(
                    ctx.send(f"The game has already started, [go to the game]({mes.jump_url})"))
            return
        else:
            embed = nextcord.Embed(
                title="New roulette game started!",
                description=f"{ctx.author.mention} have placed a bet of {amount}{currency_emoji} on {val}",
                color=color
            )
            embed.set_author(name=ctx.guild.name,
                             icon_url=ctx.guild.icon)
            embed.set_footer(
                text="Time remaining: 10 seconds after each bet (maximum 1 minute)")
            mes = await ctx.send(embed=embed)

            listener = [(ctx.author, amount, val)]
            future, postpone = create_roulette_task()
            roulette_games[ctx.guild.id] = (
                postpone, listener, mes)

            try:
                await asyncio.wait_for(future, timeout=60)
            except asyncio.TimeoutError:
                pass

        roulette_games.pop(ctx.guild.id, None)
        ran = random.randint(1, 36)
        results = []
        for _member, _amount, _arg in listener:
            for roulette_item in arguments_roulette:
                if roulette_item["input_data_condition"](_arg):
                    account = EconomyMemberDB(ctx.guild.id, _member.id)
                    if roulette_item["random_condition"](_arg, ran):
                        account["balance"] += _amount * \
                            roulette_item["multiplier"]
                        results.append(
                            f"{_member.mention} won **{_amount * roulette_item['multiplier']}**{currency_emoji}")
                    else:
                        results.append(
                            f"{_member.mention} lost **{_amount}**{currency_emoji}")
                    break
        win_color = 'red' if arguments_roulette[6]["random_condition"](
            0, ran) else 'black'
        embed = nextcord.Embed(
            title=f"The ball landed on **{win_color} {ran}**",
            description='\n'.join(results),
            color=color
        )
        embed.set_author(name=ctx.guild.name,
                         icon_url=ctx.guild.icon)
        await mes.edit(embed=embed)

    @commands.command(name="blackjack", aliases=["bj"])
    async def blackjack(self, ctx: commands.Context, amount: int):
        gdb = GuildDateBases(ctx.guild.id)
        prefix = gdb.get('prefix')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)

        if amount <= 0:
            await ctx.send(content="Specify the amount more `0`")
            raise TypeError('Planned error')
        if amount > account['balance']:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            raise TypeError('Planned error')

        account["balance"] -= amount
        bjg = BlackjackGame(ctx.author, amount)

        match bjg.is_avid_winner():
            case 2:
                await ctx.send(embed=bjg.completed_embed)
                bjg.complete()
                account["balance"] += amount
                return
            case 1:
                await ctx.send(embed=bjg.completed_embed)
                bjg.complete()
                account["balance"] += 3.5*amount
                return
            case 0:
                await ctx.send(embed=bjg.completed_embed)
                bjg.complete()
                return

        view = BlackjackView(bjg)
        await ctx.send(embed=bjg.embed, view=view)


def setup(bot):
    bot.add_cog(Economy(bot))
