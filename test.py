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




async def getRandomQuote(lang='en'):
    url = f"https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}"
    async with aiohttp.ClientSession() as session:
        try:
            res = await session.post(url)
            json = await res.json()
            return json
        except:
            return await getRandomQuote(lang)



@bot.message_command(name="Translate",default_member_permissions=8)
async def reping(inters: nextcord.Interaction, message: nextcord.Message):
    local = find(lambda lan:lan['locale']==inters.locale,languages)
    result = translator.translate(text=message.content, dest=local['google_language'])
    view = nextcord.ui.View(timeout=None)
    select = nextcord.ui.Select(
        placeholder="Will choose the appropriate language:",
        min_values=1,
        max_values=1,
        options=[
            nextcord.SelectOption(
                label=lang['native_name'],
                description=lang['language_name'],
                emoji=lang['flag'],
                value=lang['google_language']
            )
            for lang in languages[:25]
        ]
    )
    
    async def _callback(_inter: nextcord.Interaction):
        result = translator.translate(text=message.content, dest=select.values[0])
        await _inter.response.send_message(content=result.text,ephemeral=True)
    select.callback = _callback
    
    view.add_item(select)
    await inters.response.send_message(content=result.text,view=view,ephemeral=True)




@bot.slash_command(name="random-quote")
async def random_quote(
    inter: nextcord.Interaction, 
    lang=nextcord.SlashOption(
    name='language',
    description='Select the language in which you want to see the quote',
    choices={lag['native_name']:lag['google_language'] for lag in languages[:25]})
):
    await inter.response.defer(ephemeral=True)
    match lang:
        case 'ru':
            quote = await getRandomQuote(lang)
        case 'en':
            quote = await getRandomQuote(lang)
        case _:
            quote = await getRandomQuote('en')
            qt = translator.translate(quote['quoteText'],dest=lang)
            qa = translator.translate(quote['quoteAuthor'],dest=lang)
            quote['quoteText'] = qt.text
            quote['quoteAuthor'] = qa.text
    
    await inter.edit_original_message(content=f"*{quote['quoteText']}*\n\n**{quote['quoteAuthor']}**")




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

