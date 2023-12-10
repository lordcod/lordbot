import nextcord
from nextcord.ext import commands

from bot.databases.db import EconomyMembedDB,colums,GuildDateBases
from bot.resources.errors import NotActivateEconomy
from bot.resources.ether import Emoji
from bot.misc.utils import get_prefix, get_award

from time import time as tick
from typing import Optional, Union, Literal

timeout_rewards = {"daily": 86400,"weekly": 604800,"monthly": 2592000}

class MemberDB:
    def __init__(self, guild_id: int, member_id: int) -> None:
        self.guild_id = guild_id
        self.member_id = member_id
        
        self.emdb = EconomyMembedDB(guild_id,member_id)
        data = self.emdb.get()
        
        colums_name = [cl[0] for cl in colums['economic']][2:] # Get name colums from economic except guild_id and member_id 
        
        if not data:
            self.emdb.insert()
            data = self.emdb.get()
        data = list(data)[2:] # Get data from economy member except guild_id and member_id
        data = dict(zip(colums_name,data)) # Create dict in which colums_name = data_member
        self.data = data
    
    def get_leaderboards(self):
        leaderboard_ids = self.emdb.get_leaderboards()
        return leaderboard_ids
    
    def get(self,__name,__default=None):
        try:
            return self.__getitem__(__name)
        except:
            return __default
    
    def __getitem__(self, item):
        return self.data[item]
    
    def __setitem__(self, key, value):
        self.data[key] = value
        
        self.emdb.update(key, value)


class Economy(commands.Cog):
    bot: commands.Bot
    
    def __init__(self,bot: commands.Bot) -> None:
        self.bot = bot
        
        super().__init__()
    
    def cog_check(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        es = gdb.get('economic_settings')
        operate = es.get('operate',False)
        if not operate:
            raise NotActivateEconomy("Economy is not enabled on the server")
        return True
    
    
    async def handler_rewards(self,ctx: commands.Context):
        time = tick()
        account = MemberDB(ctx.guild.id,ctx.author.id)
        gdb = GuildDateBases(ctx.guild.id)
        colour = gdb.get('color')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        award = eco_sets.get(ctx.command.name,0)
        
        if award <= 0:
            await ctx.send("Unfortunately this reward is not available if you are the server administrator change the reward")
            return
        
        if (time-account.get(ctx.command.name,0)) >= 0:
            wait_long = time+timeout_rewards.get(ctx.command.name)
            
            embed = nextcord.Embed(
                title="You have received a gift",
                description=f"In size {award}{currency_emoji} come through <t:{wait_long :.0f}:R>",
                color = colour
            )
            
            account[ctx.command.name] = wait_long
            account['balance'] += award
        else:
            embed = nextcord.Embed(
                title="The reward is not available",
                description=f'Try again after <t:{account.get(ctx.command.name) :.0f}:R>',
                color = colour
            )
        await ctx.send(embed=embed)
    
    @commands.command(name='daily')
    async def daily(self,ctx: commands.Context):
        await self.handler_rewards(ctx)
    
    @commands.command(name='weekly')
    async def weekly(self,ctx: commands.Context):
        await self.handler_rewards(ctx)
    
    @commands.command(name='monthly')
    async def monthly(self,ctx: commands.Context):
        await self.handler_rewards(ctx)
    
    
    @commands.command(name="balance",aliases=["bal"])
    async def balance(self,ctx:commands.Context, member: nextcord.Member = None):
        if not member:
            member = ctx.author
        
        
        gdb = GuildDateBases(ctx.guild.id)
        colour = gdb.get('color')
        prefix = get_prefix(ctx.guild.id, markdown=True, GuildData=gdb)
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = MemberDB(ctx.guild.id,member.id)
        balance = account.get('balance',0)
        bank = account.get('bank',0)
        time = tick()
        
        description = ""
        if account.get('daily',0) < time:
            description = f"{description}— Ежедневный бонус ({prefix}daily)\n"
        if account.get('weekly',0) < time:
            description = f"{description}— Еженедельный бонус ({prefix}weekly)\n"
        if account.get('monthly',0) < time:
            description = f"{description}— Ежемесячный бонус ({prefix}monthly)\n"
        if description:
            description = f"{Emoji.award} Доступные награды:\n{description}"
        
        embed = nextcord.Embed(
            title="Баланс",
            color=colour,
            description = description,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        
        embed.add_field(
            name=f"{Emoji.money} Наличные:",
            value=f'{balance}{currency_emoji}', 
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bank} В банке:",
            value=f'{bank}{currency_emoji}',
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bagmoney} Общий баланс:",
            value=f'{balance+bank}{currency_emoji}',
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="leaderboard",aliases=["leader"])
    async def leaderboard(self, ctx: commands.Context):
        message = await ctx.send("Загрузка данных...")
        
        gdb = GuildDateBases(ctx.guild.id)
        colour = gdb.get("color")
        economy_settings: dict = gdb.get('economic_settings',{})
        currency_emoji = economy_settings.get("emoji")
        
        emdb = MemberDB(ctx.guild.id, ctx.author.id)
        leaderboard_empty = emdb.get_leaderboards()
        
        leaderboard_ids = {}
        
        for leader in leaderboard_empty[:15]:
            member_id = leader[1]
            balance = leader[2]
            bank = leader[3]
            total = balance+bank
            
            leaderboard_ids[member_id] = {
                'balance':balance,
                'bank':bank,
                'total':total
            }
        sorted_leaderboard = dict(sorted(leaderboard_ids.items(), key=lambda item: item[1]['total'], reverse=True))
        index = list(sorted_leaderboard).index(ctx.author.id)+1
        embed = nextcord.Embed(
            title="Список лидеров по балансу",
            description=f"**{ctx.author.display_name}**, Ваша позиция в топе: **{index}**",
            color=colour
        )
        sld = list(sorted_leaderboard.items())
        
        for member_id, data in sld[:10]:
            member = ctx.guild.get_member(member_id)
            if not member:
                del sorted_leaderboard[member_id]
                continue
            index = list(sorted_leaderboard).index(member_id)+1
            award = get_award(index)
            balance = data['balance']
            bank = data['bank']
            total = data['total']
            
            embed.add_field(
                name=f"{award}. {member.display_name}",
                value=(
                    f"Наличные: {balance}{currency_emoji} | В банке: {bank}{currency_emoji}"
                    "\n"
                    f"Всего: {total}{currency_emoji}"
                ),
                inline=False
            )
        
        await message.edit(content=None,embed=embed)
    
    @commands.command(name="pay")
    async def pay(self,ctx: commands.Context, member: nextcord.Member, sum: int):
        gdb = GuildDateBases(ctx.guild.id)
        colour = gdb.get('color')
        prefix = gdb.get('prefix')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        from_account = MemberDB(ctx.guild.id,ctx.author.id)
        to_account = MemberDB(ctx.guild.id,member.id)
        
        if sum <= 0:
            await ctx.send(content="Specify the amount more **0**")
            return
        elif (from_account.get('balance',0)-sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{prefix}bal`")
            return
        
        embed = nextcord.Embed(
                title="Transfer of currency", 
                color=colour,
                description=f"You were given **{sum}**{currency_emoji}"
            )
        embed.set_footer(text=f'From {ctx.author.display_name}', icon_url=ctx.author.display_avatar)
        
        await ctx.send(embed=embed)
        
        from_account["balance"] -= sum
        to_account["balance"] += sum
    
    
    @commands.command(name="deposit",aliases=["dep"])
    async def deposit(self,ctx: commands.Context, sum: Union[Literal['all'],int]):
        gdb = GuildDateBases(ctx.guild.id)
        colour = gdb.get('color')
        prefix = gdb.get('prefix')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = MemberDB(ctx.guild.id,ctx.author.id)
        balance = account.get('balance',0)
    
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
            color=colour, 
            description=f"You have transferred **{sum}**{currency_emoji} to the bank account"
        )
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    
        await ctx.send(embed=embed)
    
    @commands.command(name="withdraw",aliases=["wd"])
    async def withdraw(self,ctx: commands.Context, sum: Union[Literal['all'],int]):
        gdb = GuildDateBases(ctx.guild.id)
        colour = gdb.get('color')
        prefix = gdb.get('prefix')
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = MemberDB(ctx.guild.id,ctx.author.id)
        bank = account.get('bank',0)
    
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
            color=colour, 
            description=f"You have transferred **{sum}**{currency_emoji} to the account"
        )
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    
        await ctx.send(embed=embed)
    
    
    @commands.command(name="gift")
    @commands.has_permissions(administrator=True)
    async def gift(self,ctx: commands.Context, member: Optional[nextcord.Member], sum: int):
        if sum > 1_000_000:
            await ctx.send(f"The maximum amount for this server - {1_000_000}")
            return
        if 0 >= sum:
            await ctx.send("The amount must be positive")
            return
        
        if not member:
            member = ctx.author
        
        
        gdb = GuildDateBases(ctx.guild.id)
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = MemberDB(ctx.guild.id,member.id)
        
        account["balance"] += sum
        
        await ctx.send(f"You passed {member.display_name}, **{sum}**{currency_emoji} ")
    
    @commands.command(name="take")
    @commands.has_permissions(administrator=True)
    async def take(self,ctx: commands.Context, member: Optional[nextcord.Member], sum: int):
        if sum > 1_000_000:
            await ctx.send(f"The maximum amount for this server - {1_000_000}")
            return
        if 0 >= sum:
            await ctx.send("The amount must be positive")
            return
        
        if not member:
            member = ctx.author
        
        
        gdb = GuildDateBases(ctx.guild.id)
        eco_sets: dict = gdb.get('economic_settings')
        currency_emoji = eco_sets.get('emoji')
        account = MemberDB(ctx.guild.id,member.id)
        
        if 0 > (account.get('balance')-sum):
            await ctx.send('The operation cannot be performed because the balance will become negative during it')
            return
        
        account["balance"] -= sum
        
        await ctx.send(f"You passed `{member.display_name}`, **{sum}**{currency_emoji} ")


def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))