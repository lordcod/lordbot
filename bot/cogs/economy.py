
import nextcord
from nextcord.ext import commands
import nextcord.gateway
from nextcord.utils import escape_markdown


import random
import asyncio
import time
import orjson
from typing import Callable, Dict, List, Optional, Tuple, TypedDict, Union, Literal


from bot.databases import EconomyMemberDB, GuildDateBases
from bot.misc import logstool
from bot.resources import check
from bot.views.economy_shop import EconomyShopView
from bot.misc.lordbot import LordBot
from bot.misc.utils import clamp, randfloat, translate_flags
from bot.resources.errors import InactiveEconomy
from bot.resources.ether import Emoji
from bot.misc.utils import BlackjackGame
from bot.resources.info import DEFAULT_ECONOMY_THEFT
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


def check_prison():
    async def predicate(ctx: commands.Context) -> bool:
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        conclusion = await account.get('conclusion')
        if not conclusion or time.time() > conclusion:
            return True
        await ctx.send(f"You are in prison, and you will be in it for another <t:{conclusion :.0f}:R>.")
        return False
    return commands.check(predicate)


class Economy(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    async def cog_check(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        es = await gdb.get('economic_settings')
        operate = es.get('operate', False)
        if not operate:
            raise InactiveEconomy("Economy is disabled on the server")
        return True

    async def handle_rewards(self, ctx: commands.Context):
        loctime = time.time()
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        gdb = GuildDateBases(ctx.guild.id)

        color = await gdb.get('color')
        economic_settings: dict = await gdb.get('economic_settings')
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
            await account.set(ctx.command.name, wait_long)
            await account.increment('balance', award)
            await logstool.Logs(ctx.guild).add_currency(ctx.author, award, reason=f'{ctx.command.name} reward')
        else:
            reward_time = await account.get(ctx.command.name)
            embed = nextcord.Embed(
                title="The reward is not available",
                description=f'Try again after <t:{reward_time :.0f}:R>',
                color=color
            )

        await ctx.send(embed=embed)

    @commands.command(name='daily')
    @check_prison()
    async def daily(self, ctx: commands.Context):
        await self.handle_rewards(ctx)

    @commands.command(name='weekly')
    @check_prison()
    async def weekly(self, ctx: commands.Context):
        await self.handle_rewards(ctx)

    @commands.command(name='monthly')
    @check_prison()
    async def monthly(self, ctx: commands.Context):
        await self.handle_rewards(ctx)

    @commands.command(name='work')
    @check_prison()
    async def work(self, ctx: commands.Context):
        loctime = time.time()
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        gdb = GuildDateBases(ctx.guild.id)
        locale = await gdb.get('language')
        color = await gdb.get('color')
        work = await account.get('work', 0)
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        work_info = economic_settings.get('work')

        if loctime > work+work_info['cooldown']:
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
            account.set('work', loctime)
            account.increment('balance', amount)
        else:
            embed = nextcord.Embed(
                title="It's too early to work",
                description=f"Try again after <t:{work+work_info['cooldown'] :.0f}:R>",
                color=color
            )
        await ctx.send(embed=embed)
        await logstool.Logs(ctx.guild).add_currency(ctx.author, amount, reason='part-time job')

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self,
                      ctx: commands.Context,
                      member: Optional[nextcord.Member] = None):
        if not member:
            member = ctx.author

        loctime = time.time()

        gdb = GuildDateBases(ctx.guild.id)
        prefix = escape_markdown(await gdb.get('prefix'))
        color = await gdb.get('color')
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')

        account = EconomyMemberDB(ctx.guild.id, member.id)
        balance = await account.get('balance', 0)
        bank = await account.get('bank', 0)

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
            value=f'{balance :,}{currency_emoji}',
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bank} In bank:",
            value=f'{bank :,}{currency_emoji}',
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bagmoney} Total balance:",
            value=f'{balance+bank :,}{currency_emoji}',
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    @check_prison()
    async def shop(self, ctx: commands.Context):
        view = await EconomyShopView(ctx.guild)
        await ctx.send(embed=view.embed, view=view)

    @commands.command(name="pay")
    @check_prison()
    async def pay(self, ctx: commands.Context, member: nextcord.Member, amount: int):
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        prefix = await gdb.get('prefix')
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        from_account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        to_account = EconomyMemberDB(ctx.guild.id, member.id)

        if amount <= 0:
            await ctx.send(content="Specify the amount more **0**")
            return
        elif amount > await from_account.get('balance', 0):
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}bal`")
            return

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You were given **{amount :,}**{currency_emoji}"
        )
        embed.set_footer(
            text=f'From {ctx.author.display_name}', icon_url=ctx.author.display_avatar)

        await from_account.decline("balance", amount)
        await to_account.increment("balance", amount)

        await logstool.Logs(ctx.guild).add_currency(member, amount, reason=f'received from a {ctx.author.name} member')
        await logstool.Logs(ctx.guild).remove_currency(ctx.author, amount, reason=f'passed to the {member.name} participant')
        await ctx.send(embed=embed)

    @commands.command(name="deposit", aliases=["dep"])
    @check_prison()
    async def deposit(self, ctx: commands.Context, amount: Union[Literal['all'], int]):
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        prefix = await gdb.get('prefix')
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        balance = await account.get('balance', 0)

        if amount == "all":
            amount = balance

        if amount <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if amount > balance:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            return

        account.decline('balance', amount)
        account.increment('bank', amount)

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You have transferred **{amount :,}**{currency_emoji} to the bank account"
        )
        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="withdraw", aliases=["wd"])
    async def withdraw(self, ctx: commands.Context, amount: Union[Literal['all'], int]):
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        prefix = await gdb.get('prefix')
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        bank = await account.get('bank', 0)

        if amount == "all":
            amount = bank
        if amount <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if amount > bank:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            return

        await account.increment('balance', amount)
        await account.decline('bank', amount)

        embed = nextcord.Embed(
            title="Transfer of currency",
            color=color,
            description=f"You have transferred **{amount :,}**{currency_emoji} to the account"
        )
        embed.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="gift")
    @commands.has_permissions(administrator=True)
    async def gift(self, ctx: commands.Context, member: Optional[nextcord.Member], amount: int, *, flags: translate_flags = {}):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, member.id)

        if 0 >= amount:
            await ctx.send("The amount must be positive")
            return

        if flags.get('bank'):
            await account.increment('bank', amount)
        else:
            await account.increment('balance', amount)

        await ctx.send(f"You have transferred the amount of **{amount :,}**{currency_emoji} to {member.display_name}")
        await logstool.Logs(ctx.guild).add_currency(member, amount, moderator=ctx.author)

    @commands.command(name="take")
    @commands.has_permissions(administrator=True)
    async def take(self, ctx: commands.Context, member: Optional[nextcord.Member], amount: Union[Literal['all'], int], *, flags: translate_flags = {}):
        if not member:
            member = ctx.author

        gdb = GuildDateBases(ctx.guild.id)
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        account = EconomyMemberDB(ctx.guild.id, member.id)
        bank = await account.get('bank')
        balance = await account.get('balance')

        if amount != 'all' and 0 >= amount:
            await ctx.send("The amount must be positive")
            return

        if flags.get('bank'):
            if amount == 'all':
                amount = bank
            if amount > bank:
                await ctx.send('The operation cannot be performed because the bank balance will become negative during it')
                return

            await account.decline('bank', amount)
        else:
            if amount == 'all':
                amount = balance
            if amount > balance:
                await ctx.send('The operation cannot be performed because the balance will become negative during it')
                return

            await account.decline('balance', amount)

        await ctx.send(f"You have withdrawn an amount of **{amount :,}**{currency_emoji} from {member.display_name}")
        await logstool.Logs(ctx.guild).remove_currency(member, amount, moderator=ctx.author)

    @commands.command()
    @check_prison()
    async def rob(self, ctx: commands.Context, member: nextcord.Member):
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        theft_data = economic_settings.get('theft', DEFAULT_ECONOMY_THEFT)
        scope = (theft_data['time_prison']['max'] -
                 theft_data['time_prison']['min'] /
                 theft_data['time_prison']['adaptive'])
        conclusion = (
            time.time() +
            theft_data['time_prison']['adaptive'] *
            random.randint(1, scope+1)
        )
        thief_account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        victim_account = EconomyMemberDB(ctx.guild.id, member.id)

        thief_rob = await thief_account.get('rob')
        thief_balance = await thief_account.get('balance')

        victim_balance = await victim_account.get('balance')

        if thief_rob+theft_data['cooldown'] > time.time():
            embed = nextcord.Embed(
                title="Robbery",
                description=f"{ctx.author.mention}, You can rob now, come through <t:{thief_rob+theft_data['cooldown'] :.0f}:R>.",
                color=color
            )
            await ctx.send(embed=embed)
            return

        thief_account['rob'] = time.time()
        win_chance = clamp(
            0.1, thief_balance/(victim_balance+thief_balance), 0.75)
        if member.status != nextcord.Status.offline:
            win_chance -= 0.05
        chance = random.random()
        if win_chance > chance:
            debt = win_chance * \
                victim_balance * 1/2
            if debt >= thief_balance:
                calculated_debt = (
                    thief_balance * .6
                    * debt * .2
                    * randfloat(.8, 1.2)
                )
                embed = nextcord.Embed(
                    title="Robbery",
                    description=f"{ctx.author.mention}, you were able to steal an {calculated_debt: ,.0f}{currency_emoji}, but the victim lost the {debt: ,.0f}{currency_emoji}.",
                    color=color
                )

                await thief_account.increment('balance', calculated_debt)
                await victim_account.decline('balance', debt)
                await logstool.Logs(ctx.guild).add_currency(ctx.author, calculated_debt, reason='a successful attempt at theft')
                await logstool.Logs(ctx.guild).remove_currency(member, debt, reason='a successful attempt at theft')
            else:
                embed = nextcord.Embed(
                    title="Robbery",
                    description=f"{ctx.author.mention}, you were able to steal an {debt: ,.0f}{currency_emoji}.",
                    color=color
                )

                await thief_account.increment('balance', debt)
                await victim_account.decline('balance', debt)
                await logstool.Logs(ctx.guild).add_currency(ctx.author, debt, reason='a successful attempt at theft')
                await logstool.Logs(ctx.guild).remove_currency(member, debt, reason='a successful attempt at theft')
        else:
            debt = (1-win_chance) * thief_account['balance'] * 1/2
            embed = nextcord.Embed(
                title="Robbery",
                description=(f"{ctx.author.mention}, you couldn't steal anything during the robbery, but you lost {debt: ,.0f}{currency_emoji}.\n"
                             f"And you were also put in jail for a <t:{conclusion :.0f}:R>."),
                color=color
            )

            await thief_account.set('conclusion', conclusion)
            await victim_account.decline('balance', debt)
            await logstool.Logs(ctx.guild).remove_currency(ctx.author, debt, reason='a failed theft attempt')
        await ctx.send(embed=embed)

    @commands.command(name="roulette", aliases=["rou"])
    async def roulette(self, ctx: commands.Context, amount: int, *, val: str):
        val = val.lower()
        gdb = GuildDateBases(ctx.guild.id)
        prefix = await gdb.get('prefix')
        color = await gdb.get('color')
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        bet_info = economic_settings.get('bet')
        _min_bet = bet_info.get('min')
        _max_bet = bet_info.get('max')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)
        balance = await account.get('balance')

        if not is_valid_roulette_argument(val):
            await ctx.send(content=f"An incorrect value has been entered for the roulette game, use the command `{prefix}help {ctx.command.name}` to find out the arguments")
            raise TypeError('Planned error(invalid roulette)')
        if amount <= 0:
            await ctx.send(content="Specify the amount more `0`")
            raise TypeError('Planned error(negative amount)')
        if amount > balance:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}balance`")
            raise TypeError('Planned error(There are not enough funds)')
        if not _max_bet >= amount >= _min_bet:
            await ctx.send(content=f"The maximum bid: {_max_bet}{currency_emoji}\nThe minimum bid: {_min_bet}{currency_emoji}\nYour bid: {amount}{currency_emoji}")
            raise TypeError('Planned error(Betting violations)')

        account.increment("balance", amount)
        await logstool.Logs(ctx.guild).remove_currency(ctx.author, amount, reason='the beginning of the roulette game')

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
                        results.append(
                            f"{_member.mention} won **{_amount * roulette_item['multiplier'] :,}**{currency_emoji}")
                        await account.increment(
                            "balance", _amount * roulette_item["multiplier"])
                        await logstool.Logs(ctx.guild).add_currency(_member,
                                                                    _amount *
                                                                    roulette_item["multiplier"],
                                                                    reason='the game of roulette won')
                    else:
                        results.append(
                            f"{_member.mention} lost **{_amount :,}**{currency_emoji}")
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
        prefix = await gdb.get('prefix')
        economic_settings: dict = await gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')
        bet_info = economic_settings.get('bet')
        _min_bet = bet_info.get('min')
        _max_bet = bet_info.get('max')
        account = EconomyMemberDB(ctx.guild.id, ctx.author.id)

        if amount <= 0:
            await ctx.send("Specify the amount more `0`")
            raise TypeError('Planned error(negative amount)')
        if amount > account['balance']:
            await ctx.send(f"Not enough funds to check your balance use `{prefix}balance`")
            raise TypeError('Planned error(negative amount)')
        if not _max_bet >= amount >= _min_bet:
            await ctx.send(f"The maximum bid: {_max_bet}{currency_emoji}\n"
                           f"The minimum bid: {_min_bet}{currency_emoji}\n"
                           f"Your bid: {amount}{currency_emoji}")
            raise TypeError('Planned error(Betting violations)')

        bjg = BlackjackGame(ctx.author, amount)
        await account.decline("balance", amount)
        await logstool.Logs(ctx.guild).remove_currency(ctx.author, amount, reason='the beginning of the blackjack game')

        if bjg.is_avid_winner() is not None:
            await ctx.send(embed=bjg.completed_embed)
            match bjg.is_avid_winner():
                case 2:
                    await account.increment("balance", amount)
                    await logstool.Logs(ctx.guild).add_currency(ctx.author, amount, reason='draw at blackjack')
                case 1:
                    await account.increment("balance", 3.5*amount)
                    await logstool.Logs(ctx.guild).add_currency(ctx.author, amount, reason='a golden point in blackjack. victory')
            bjg.complete()
            return

        view = BlackjackView(bjg)
        await ctx.send(embed=bjg.embed, view=view)

    @staticmethod
    def get_slots_embed(member: nextcord.Member, color: int, results: list) -> nextcord.Embed:
        embed = nextcord.Embed(
            title='S L O T S',
            description='\n'.join(' | '.join(res) for res in results),
            color=color
        )
        embed.set_footer(text=member, icon_url=member.display_avatar)
        return embed

    @commands.command()
    @check.team_only()
    async def slots(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')

        emojis = ["⭐", "7️⃣", "💰", "🫡", "💀", "🎁", "🎉", "🥺"]
        results = (
            ['◾', '◾', '◾'],
            ['◾', '◾', '◾'],
            ['◾', '◾', '◾']
        )

        embed = self.get_slots_embed(ctx.author, color, results)
        message = await ctx.send(embed=embed)

        for _ in range(6):
            await asyncio.sleep(0.4)
            results = (
                [random.choice(emojis) for _ in range(3)],
                results[0],
                results[1]
            )
            embed = self.get_slots_embed(ctx.author, color, results)
            await message.edit(embed=embed)

        await asyncio.sleep(0.55)

        results[2][1] = results[1][1]
        results[1][1] = results[0][1]
        results[0][1] = random.choice(emojis)

        results[2][2] = results[1][2]
        results[1][2] = results[0][2]
        results[0][2] = random.choice(emojis)

        embed = self.get_slots_embed(ctx.author, color, results)
        await message.edit(embed=embed)

        await asyncio.sleep(0.7)

        results[2][2] = results[1][2]
        results[1][2] = results[0][2]
        results[0][2] = random.choice(emojis)

        embed = self.get_slots_embed(ctx.author, color, results)
        await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
