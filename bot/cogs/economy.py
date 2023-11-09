import nextcord
from nextcord.ext import commands
from typing import Any, Dict,Union
from random import randint
from time import time as tick
from bot.databases.db import GuildDateBases
from bot.resources.errors import NotActivateEconomy

timeout_rewards = {"daily": 86400,"weekly": 604800,"monthly": 2592000}

class EconomyGuildDB():
    def __init__(self,guild_id) -> None:
        self.guild_id = guild_id
    
    def economy_settings(
        self
    ) -> Dict[str,int]:
        gdb = GuildDateBases(self.guild_id)
        return gdb.get('economy_settings',{})
    
    def get_economy_db(
        self,
    ) -> Dict[int,Dict[str,int]]:
        gdb = GuildDateBases(self.guild_id)
        return gdb.get('economy',{})
    
    def get_member_account(
        self,
        member_id: int
    ) -> Dict[str,int]:
        ed = self.get_economy_db()
        
        if member_id not in ed:
            ed[member_id] = {
                "balance":0,
                "daily":0,
                "weekly":0,
                "monthly":0
            }
        
        return ed[member_id]
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        pass



class Economy(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
    
    def work_economy():
        def wrapped(ctx: commands.Context):
            gsdb = EconomyGuildDB(ctx.guild.id)().get_economy_settings(guild_id=ctx.guild.id)
            if not gsdb:
                raise NotActivateEconomy("Economy is not enabled on the server")
            return True
        return commands.check(wrapped)
    
    @commands.command(name='daily')
    @work_economy()
    async def daily(self,ctx: commands.Context):
        account = EconomyGuildDB(ctx.guild.id).get_member_account(ctx.author.id)
        economy_settings = EconomyGuildDB(ctx.guild.id).get_economy_settings(ctx.guild.id)
        
        time = tick()
        balance = account.get('balance',0)
        
        if (time-account.get(ctx.command.name)) >= 0:
            embed = nextcord.Embed(
                title="You have received a gift",
                description=f"In size {economy_settings.get(ctx.command.name)} come through <t:{time.time()+timeout_rewards.get(ctx.command.name):.0f}:R>",
                color = 0xF5740E
            )
            
            account[ctx.command.name] = time+timeout_rewards.get(ctx.command.name)
            account['balance'] = balance+economy_settings.get(ctx.command.name)
            await ctx.send(embed=embed)
        else:
                embed = nextcord.Embed(
                    title="The reward is not available",
                    description=f'Try again after <t:{account.get(ctx.command.name) :.0f}:R>'
                )
                embed.color = 0xF50E85
                
                await ctx.send(embed=embed)
    
    @commands.command(name='weekly')
    @work_economy()
    async def weekly(self,ctx: commands.Context):
        account = EconomyGuildDB(ctx.guild.id).get_member_account(ctx.author.id)
        economy_settings = EconomyGuildDB(ctx.guild.id).get_economy_settings(ctx.guild.id)
        
        time = tick()
        balance = account.get('balance',0)
        
        if (time-account.get(ctx.command.name)) >= 0:
            embed = nextcord.Embed(
                title="You have received a gift",
                description=f"In size {economy_settings.get(ctx.command.name)} come through <t:{time.time()+timeout_rewards.get(ctx.command.name):.0f}:R>",
                color = 0xF5740E
            )
            
            account[ctx.command.name] = time+timeout_rewards.get(ctx.command.name)
            account['balance'] = balance+economy_settings.get(ctx.command.name)
            await ctx.send(embed=embed)
        else:
                embed = nextcord.Embed(
                    title="The reward is not available",
                    description=f'Try again after <t:{account.get(ctx.command.name) :.0f}:R>'
                )
                embed.color = 0xF50E85
                
                await ctx.send(embed=embed)
    
    @commands.command(name='monthly')
    @work_economy()
    async def monthly(self,ctx: commands.Context):
        account = EconomyGuildDB(ctx.guild.id).get_member_account(ctx.author.id)
        economy_settings = EconomyGuildDB(ctx.guild.id).get_economy_settings(ctx.guild.id)
        
        time = tick()
        balance = account.get('balance',0)
        
        if (time-account.get(ctx.command.name)) >= 0:
            embed = nextcord.Embed(
                title="You have received a gift",
                description=f"In size {economy_settings.get(ctx.command.name)} come through <t:{time.time()+timeout_rewards.get(ctx.command.name):.0f}:R>",
                color = 0xF5740E
            )
            
            account[ctx.command.name] = time+timeout_rewards.get(ctx.command.name)
            account['balance'] = balance+economy_settings.get(ctx.command.name)
            await ctx.send(embed=embed)
        else:
                embed = nextcord.Embed(
                    title="The reward is not available",
                    description=f'Try again after <t:{account.get(ctx.command.name) :.0f}:R>'
                )
                embed.color = 0xF50E85
                
                await ctx.send(embed=embed)
    
    @commands.command(name="balance",aliases=["bal"])
    @work_economy()
    async def balance(self,ctx:commands.Context, user: nextcord.Member = None):
        if not user:
            user = ctx.author
        
        account = EconomyGuildDB(ctx.guild.id).get_member_account(ctx.author.id)
        time = tick()
        balance = account.get('balance',0)
        
        description = ""
        if account.get('daily',0) < time:
            description = f"{description}— Ежедневный бонус (\{self.bot.command_prefix}daily)\n"
        if account.get('weekly',0) < time:
            description = f"{description}— Еженедельный бонус (\{self.bot.command_prefix}weekly)\n"
        if account.get('monthly',0) < time:
            description = f"{description}— Ежемесячный бонус (\{self.bot.command_prefix}monthly)\n"
        if description:
            description = f"<a:award:1135909374112579724>Доступные награды:\n{description}"
        
        embed = nextcord.Embed(
            title="Баланс",
            color=0xE9139B,
            description = description,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_author(name=user.name, icon_url=user.avatar.url)
    
        embed.add_field(name="<:money:1135902853060362240>Наличные:",
                        value=balance['balance'], inline=True)
        embed.add_field(name="<:bank:1135902850703175731>В банке:",
                        value=balance['bank'], inline=True)
        embed.add_field(name="<:bagmoney:1135902854696157245>Общий баланс:",
                        value=balance['bank']+balance['balance'], inline=False)
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))