import nextcord
from nextcord.ext import commands
from typing import Any, Dict,Union
from random import randint
from time import time as tick
from bot.databases.db import EconomyMembedDB,colums,GuildDateBases
from bot.resources.errors import NotActivateEconomy
from bot.resources.languages import Emoji

timeout_rewards = {"daily": 86400,"weekly": 604800,"monthly": 2592000}

class MemberDB:
    def __init__(self, guild_id: int, member_id: int) -> None:
        self.guild_id = guild_id
        self.member_id = member_id
        data = EconomyMembedDB.get(guild_id,member_id)
        colums_name = [cl[0] for cl in colums['economic']][2:]
        
        if not data:
            EconomyMembedDB.insert(guild_id,member_id)
            data = EconomyMembedDB.get(guild_id,member_id)
        data = list(data)[2:]
        data = dict(zip(colums_name,data))
        self.data = data
    
    def get(self,__name,__default=None):
        try:
            return self.__getitem__(__name)
        except:
            return __default
    
    def __getitem__(self, item):
        return self.data[item]
    
    def __setitem__(self, key, value):
        self.data[key] = value
        
        EconomyMembedDB.update_list(self.guild_id,self.member_id,self.data)


class Economy(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
    
    def work_economy():
        def wrapped(ctx: commands.Context):
            settings = GuildDateBases(ctx.guild.id).get('economic_settings')
            if not settings:
                raise NotActivateEconomy("Economy is not enabled on the server")
            return True
        return commands.check(wrapped)
    
    
    async def handler_rewards(self,ctx: commands.Context):
        time = tick()
        account = MemberDB(ctx.guild.id,ctx.author.id)
        eco_sets = GuildDateBases(ctx.guild.id).get('economic_settings',{})
        award = eco_sets.get(ctx.command.name,0)
        
        if award <= 0:
            await ctx.send("Unfortunately this reward is not available if you are the server administrator change the reward")
            return
        
        if (time-account.get(ctx.command.name,0)) >= 0:
            wait_long = time+timeout_rewards.get(ctx.command.name)
            
            embed = nextcord.Embed(
                title="You have received a gift",
                description=f"In size {award} come through <t:{wait_long :.0f}:R>",
                color = 0xF5740E
            )
            
            account[ctx.command.name] = wait_long
            account['balance'] += award
        else:
            embed = nextcord.Embed(
                title="The reward is not available",
                description=f'Try again after <t:{account.get(ctx.command.name) :.0f}:R>',
                color = 0xF50E85
            )
        await ctx.send(embed=embed)
    
    @commands.command(name='daily')
    @work_economy()
    async def daily(self,ctx: commands.Context):
        await self.handler_rewards(ctx)
    
    @commands.command(name='weekly')
    @work_economy()
    async def weekly(self,ctx: commands.Context):
        await self.handler_rewards(ctx)
    
    @commands.command(name='monthly')
    @work_economy()
    async def monthly(self,ctx: commands.Context):
        await self.handler_rewards(ctx)
    
    
    @commands.command(name="balance",aliases=["bal"])
    @work_economy()
    async def balance(self,ctx:commands.Context, member: nextcord.Member = None):
        if not member:
            print('No member')
            member = ctx.author
        
        time = tick()
        account = MemberDB(ctx.guild.id,member.id)
        balance = account.get('balance',0)
        bank = account.get('bank',0)
        
        description = ""
        if account.get('daily',0) < time:
            description = f"{description}— Ежедневный бонус (\{self.bot.command_prefix}daily)\n"
        if account.get('weekly',0) < time:
            description = f"{description}— Еженедельный бонус (\{self.bot.command_prefix}weekly)\n"
        if account.get('monthly',0) < time:
            description = f"{description}— Ежемесячный бонус (\{self.bot.command_prefix}monthly)\n"
        if description:
            description = f"{Emoji.award}Доступные награды:\n{description}"
        
        embed = nextcord.Embed(
            title="Баланс",
            color=0xE9139B,
            description = description,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        
        embed.add_field(
            name=f"{Emoji.money}Наличные:",
            value=balance, 
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bank}В банке:",
            value=bank,
            inline=True
        )
        embed.add_field(
            name=f"{Emoji.bagmoney}Общий баланс:",
            value=balance+bank,
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="pay")
    @work_economy()
    async def pay(self,ctx: commands.Context, member: nextcord.Member, sum: int):
        from_account = MemberDB(ctx.guild.id,ctx.author.id)
        to_account = MemberDB(ctx.guild.id,member.id)
        
        if sum <= 0:
            await ctx.send(content="Specify the amount more **0**")
            return
        elif (from_account.get('balance',0)-sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{self.bot.command_prefix}bal`")
            return
        
        embed = nextcord.Embed(
                title="Transfer of currency", 
                color=nextcord.Colour(0x14db6b),
                description=f"You were given **{sum}$**"
            )
        embed.set_author(name=f'{member.display_name} это вам!', icon_url=member.display_avatar)
        embed.set_footer(text=f'От {ctx.author.display_name}', icon_url=ctx.author.display_avatar)
        
        await ctx.send(embed=embed)
        
        from_account["balance"] = from_account["balance"] - sum
        to_account["balance"] = to_account["balance"] + sum
    
    
    
    @commands.command(name="deposit",aliases=["dep"])
    @work_economy()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def dep(self,ctx: commands.Context, sum: str):
        account = MemberDB(ctx.guild.id,ctx.author.id)
        balance = account.get('balance',0)
    
        if not sum.isdigit():
            if sum == "all":
                sum = balance
            else:
                await ctx.send(f"You have entered an invalid argument, use the command so `{self.bot.command_prefix}deposit sum`")
                return
        sum = int(sum)
    
        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if (balance - sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{self.bot.command_prefix}bal`")
            return
        account['balance'] = account['balance'] - sum
        account['bank'] = account['bank'] + sum

        embed = nextcord.Embed(
            title="Transfer of currency", 
            colour=nextcord.Colour(0x9aecce), 
            description=f"You have transferred **{sum}$** to the bank account"
        )
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    
        await ctx.send(embed=embed)
    
    @commands.command(name="withdraw",aliases=["wd"])
    @work_economy()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def withdraw(self,ctx: commands.Context, sum: str):
        account = MemberDB(ctx.guild.id,ctx.author.id)
        bank = account.get('bank',0)
    
        if not sum.isdigit():
            if sum == "all":
                sum = bank
            else:
                await ctx.send(f"You have entered an invalid argument, use the command so `{self.bot.command_prefix}deposit sum`")
                return
        sum = int(sum)
    
        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        if (bank - sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{self.bot.command_prefix}bal`")
            return
        account['balance'] = account['balance'] + sum
        account['bank'] = account['bank'] - sum

        embed = nextcord.Embed(
            title="Transfer of currency", 
            colour=nextcord.Colour(0x9aecce), 
            description=f"You have transferred {sum}$ to the account"
        )
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    
        await ctx.send(embed=embed)
    
    
    @commands.command(name="gift")
    @work_economy()
    @commands.has_permissions(administrator=True)
    async def gift(self,ctx: commands.Context, member: nextcord.Member, sum: int):
        account = MemberDB(ctx.guild.id,member.id)
        
        account["balance"] += sum
        
        await ctx.send(f"You passed {member.mention}, **{sum}$** ")
    
    @commands.command(name="take")
    @work_economy()
    @commands.has_permissions(administrator=True)
    async def take(self,ctx: commands.Context, member: nextcord.Member = None, sum: int = None):
        account = MemberDB(ctx.guild.id,member.id)
        
        account["balance"] -= sum
        
        await ctx.send(f"You passed {member.mention}, **{sum}$** ")
    

def setup(bot):
    bot.add_cog(Economy(bot))