class Tricky():
    def __init__(self,val) -> None:
        self.val = val
    
    def __str__(self) -> str:
        return self.val
    
    def __call__(self, val):
        return val

obj = Tricky(' b1')


if __name__ == "__main__":
    print(obj)     # prints 1
    print(obj(5))  # prints 5



    @commands.command(name="pay")
    @work_economy()
    async def pay(self,ctx: commands.Context, member: nextcord.Member = None, sum: int = None):
        if not (member and sum):
            return
        balance_guild_db = get_balance_bd(str(ctx.guild.id))
        my_balance = balance_guild_db[str(ctx.author.id)]
        his_balance = balance_guild_db[str(member.id)]
        
        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
        elif (my_balance['balance'] - sum) > 0:
            embed = nextcord.Embed(
            title="Transfer of currency", 
            color=nextcord.Colour(0x14db6b),
            description=f"You passed {sum}$ to the player {member.mention}")
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)
            
            my_balance["balance"] = my_balance["balance"] - sum
            his_balance["balance"] = his_balance["balance"] + sum
        else:
            await ctx.send(content=f"Not enough funds to check your balance use `{self.bot.command_prefix}bal`")
        set_balance_bd(ctx.guild.id,balance_guild_db)
    
    @commands.command(name="deposit",aliases=["dep"])
    @work_economy()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def dep(self,ctx: commands.Context, sum=None):
        balance_guild_db = get_balance_bd(str(ctx.guild.id))
        balance = balance_guild_db[str(ctx.author.id)]
    
        try:
            sum = int(sum)
        except:
            if sum == "all":
                sum = balance['balance']
            else:
                await ctx.send(f"You have entered an invalid argument, use the command so `{self.bot.command_prefix}deposit sum`")
                return
    
        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
        elif (balance['balance'] - sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{self.bot.command_prefix}bal`")
        else:
            balance['balance'] = balance['balance'] - sum
            balance['bank'] = balance['bank'] + sum
    
            embed = nextcord.Embed(
            title="Transfer of currency", 
            colour=nextcord.Colour(0x9aecce), 
            description=f"You have transferred {sum}$ to the bank account")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    
            await ctx.send(embed=embed)
        set_balance_bd(ctx.guild.id,balance_guild_db)
    
    @commands.command(name="withdraw",aliases=["wd"])
    @work_economy()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def withdraw(self,ctx: commands.Context, sum=None):
        balance_guild_db = get_balance_bd(str(ctx.guild.id))
        balance = balance_guild_db[str(ctx.author.id)]
    
        try:
            sum = int(sum)
        except:
            if sum == "all":
                sum = balance['bank']
            else:
                await ctx.send(f"You have entered an invalid argument, use the command so `{self.bot.command_prefix}deposit sum`")
                return
    
        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
        elif (balance['bank'] - sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{self.bot.command_prefix}bal`")
        else:
            balance['bank'] = balance['bank'] - sum
            balance['balance'] = balance['balance'] + sum
    
            embed = nextcord.Embed(
            title="Transfer of currency", 
            colour=nextcord.Colour(0x9aecce),
            description=f"You have transferred {sum}$ to the account")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    
            await ctx.send(embed=embed)
        set_balance_bd(ctx.guild.id,balance_guild_db)
    
    @commands.command(name="gift")
    @work_economy()
    @commands.has_permissions(administrator=True)
    async def gift(self,ctx: commands.Context, member: nextcord.Member = None, sum: int = None):
        balance_guild_db = get_balance_bd(str(ctx.guild.id))
        if member and int(sum):
            balance = balance_guild_db[str(member.id)]
            balance["balance"] = balance["balance"] + sum
            await ctx.send(f"You passed {member.mention}, {sum}$ ")
        set_balance_bd(ctx.guild.id,balance_guild_db)
    
    @commands.command(name="take")
    @work_economy()
    @commands.has_permissions(administrator=True)
    async def take(self,ctx: commands.Context, member: nextcord.Member = None, sum: int = None):
        balance_guild_db = get_balance_bd(str(ctx.guild.id))
        if member and sum:
            balance = balance_guild_db[str(member.id)]
            balance["balance"] = balance["balance"] - sum
            await ctx.send(f"You passed {member.mention}, {sum}$ ")
        set_balance_bd(ctx.guild.id,balance_guild_db)
    
    @commands.command(name="roulette",aliases=["rou"])
    @work_economy()
    @commands.cooldown(rate=1, per=6.75, type=commands.BucketType.user)
    async def roulette(self,ctx: commands.Context, sum=None, *, val=None):
        balance_guild_db = get_balance_bd(str(ctx.guild.id))
        balance = balance_guild_db[str(ctx.author.id)]
        ran = randint(1, 36)
        is_int = None
        winner = False
        
        try:
            sum = int(sum)
        except:
            if sum == "all":
                sum = balance['balance']
            else:
                embed = nextcord.Embed(
                    title="Here is a list of arguments for the game",
                    description=f"You have entered an invalid argument, use the command so `{self.bot.command_prefix}roulette sum argument`")
                await ctx.send(embed=embed)
                return
        try:
            int(val)
            is_int = True
        except:
            is_int = False
        
        if sum <= 0:
            await ctx.send(content="Specify the amount more `0`")
            return
        elif (balance['balance'] - sum) < 0:
            await ctx.send(content=f"Not enough funds to check your balance use `{self.bot.command_prefix}bal`")
            return
        
        argument_roulette = [
            {
                "input_data_condition":is_int and int(val) > 0 and int(val) <= 36,
                "random_condition":ran == val,
                "multiplier":35,
            },
            {
                "input_data_condition":val == "1 to 12",
                "random_condition":ran >= 1 and ran <= 12,
                "multiplier":3,
            },
            {
                "input_data_condition":val == "13 to 24",
                "random_condition":ran >= 13 and ran <= 24,
                "multiplier":3,
            },
            {
                "input_data_condition":val == "25 to 36",
                "random_condition":ran >= 25 and ran <= 36,
                "multiplier":3,
            },
            {
                "input_data_condition":val == "1 to 18",
                "random_condition":ran >= 1 and ran <= 18,
                "multiplier":2,
            },
            {
                "input_data_condition":val == "19 to 36",
                "random_condition":ran >= 19 and ran <= 36,
                "multiplier":2,
            },
            {
                "input_data_condition":val == "red",
                "random_condition":ran in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
                "multiplier":2,
            },
            {
                "input_data_condition":val == "black",
                "random_condition":ran in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
                "multiplier":2,
            },
            {
                "input_data_condition":val == "even",
                "random_condition":ran % 2 == 0,
                "multiplier":2,
            },
            {
                "input_data_condition":val == "odd",
                "random_condition":ran % 2 == 1,
                "multiplier":2,
            },
        ]
        
        for dict_arguments_roulette in argument_roulette:
            if dict_arguments_roulette["input_data_condition"]:
                if dict_arguments_roulette["random_condition"]:
                    balance["balance"] = balance["balance"] + (sum * dict_arguments_roulette["multiplier"] - sum)
                    winner = True
                    break
        
        if winner:
            await ctx.send(f"You won, the number fell out **{ran}**")
        else:
            await ctx.send(f"You lost, the number fell out **{ran}**")
            balance["balance"] = balance["balance"] - sum
        
        set_balance_bd(ctx.guild.id,balance_guild_db)

