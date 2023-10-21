import nextcord
from nextcord.ext import (commands,application_checks,tasks)
from nextcord import utils
from nextcord.utils import get

import asyncio,orjson,random,googletrans,datetime as dtt,\
pickle,time,threading,os,aiohttp,io,recaptcha
from config import *

translator = googletrans.Translator()

DEFAULT_PREFIX = '.'

bot = commands.Bot(command_prefix=DEFAULT_PREFIX,intents=nextcord.Intents.all())

def generate_message(content):
    message = {}
    try:
        content = orjson.loads(content)
        
        message['embeds'] = []
        if "embeds" in content and type(content["embeds"]) == dict:
            for em in content["embeds"]:
                nextcord.Embed.from_dict(em)
        
        if "content" in message:
            message['content'] = content['content']
        
        if "flags" in message:
            message['flag'] = nextcord.MessageFlags()
            message['flag'].value = content["flags"]
    except orjson.JSONDecodeError:
        message['content'] = content
    return message


forum_messages = {
    'channel_id':{'embed'}
}
auto_reactions = {
    'channel_id':['reaction']
}
laung_table = {
    'channel_id':'lang',
    1095713596790550592:'ru'
}


@bot.event
async def on_ready():
    print(f"The bot is registered as {bot.user}")

@bot.event
async def on_disconnect():
    print("Bot is disconnect")


@bot.event
async def on_command_error(ctx: commands.Context, error):
    print(f"[HANDLER][on_command_error][{ctx.command.name}]: {error}")

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    print(f"[HANDLER][on_application_command_error][{interaction.application_command}]: {error}")


@bot.event
async def on_interaction(interaction:nextcord.Interaction):
    print(interaction.type)
    await bot.process_application_commands(interaction)

@bot.event
async def on_thread_create(thread:nextcord.Thread):
    if thread.parent.id not in forum_messages:
        return

    mes = forum_messages[thread.parent.id]
    await thread.send(embed=nextcord.Embed(**mes))

@bot.event
async def on_member_update(before:nextcord.Member,after:nextcord.Member):
    roles_b = before.roles
    roles_a = after.roles
    remove = list(set(roles_b)-set(roles_a))
    add = list(set(roles_a)-set(roles_b))

    if add:
        print(f'У {before.name} добавили роль {add[0].name}')
    elif remove:
        print(f'У {before.name} удалили роль {remove[0].name}')

@bot.event
async def on_message(message: nextcord.Message):
    if message.author.bot:
        return
    
    if message.channel.id in auto_reactions:
        reacts = auto_reactions[message.channel.id]
        for rea in reacts:
            await message.add_reaction(rea)
    
    if message.channel.id in laung_table:
        lang = laung_table[message.channel.id]
        result = translator.translate(message.content,dest=lang)
        if result.src != lang:
            embed = nextcord.Embed(
                title="Авто-Перевод",
                description=f'### {result.text}',
                color=0xa17fe0
            )
            embed._fields = [
                {
                    'name':f'Переведено c {laungs[result.src]}',
                    'value':f'',
                    'inline':True
                },
                {
                    'name':f'Переведено на {laungs[result.dest]}',
                    'value':f'',
                    'inline':True
                },
            ]
            embed.set_footer(text='Powered by LordBot',icon_url=bot.user.avatar.url)
            await message.channel.send(embed=embed)
    
    await bot.process_commands(message)



async def acc_activiti(interaction: nextcord.Interaction, arg: str):
    if interaction.guild is None:
        await interaction.response.send_autocomplete([])
        return
    
    list = {act['label']:str(act['id']) for act in activities_list[:25]}
    if not arg:
        await interaction.response.send_autocomplete(list)
        return
    get_near = {}
    for act in list:
        if act.lower().startswith(arg.lower()):
            get_near[act]=list[act]
    await interaction.response.send_autocomplete(get_near)

@bot.slash_command(name="activiti")
@application_checks.guild_only()
async def activiti(interaction:nextcord.Interaction,
    voice:nextcord.VoiceChannel=nextcord.SlashOption(name="voice"),
    act=nextcord.SlashOption(
        name="activiti",
        autocomplete=True,
        autocomplete_callback=acc_activiti,),
):
    try:
        inv = await voice.create_invite(
            target_type=nextcord.InviteTarget.embedded_application,
            target_application_id=act
        )
    except:
        await interaction.response.send_message(content="This activity is unavailable or does not work")
        return
    view = nextcord.ui.View(timeout=None)
    view.add_item(nextcord.ui.Button(label="Activiti",emoji="<:rocket:1154866304864497724>",url=inv.url))
    emb = nextcord.Embed(title="**Активность успешно создана!**",color=0xfff8dc,description="Однако некоторые виды активностей могут быть недоступны для вашего сервера, если уровень бустов не соответствует требованиям активности.")
    await interaction.response.send_message(embed=emb,view=view,ephemeral=True)


@bot.command()
async def say(ctx:commands.Context, *, message: str=None):
    files = []
    for attach in ctx.message.attachments:
        data = io.BytesIO(await attach.read())
        files.append(nextcord.File(data, attach.filename))
    
    res = generate_message(message)
    ctx.send(**res,files=files)
    
    await ctx.message.delete()

@bot.command()
async def captcha(ctx:commands.Context):
    data,text = recaptcha.generator(random.randint(3,7))
    print(f"Captcha text: {text}")
    image_file = nextcord.File(data,filename="cap.png",description="Captcha",spoiler=True)
    await ctx.send(file=image_file)
    
    def check(mes:nextcord.Message):
        return mes.channel==ctx.channel and mes.author==ctx.author
    mes:nextcord.Message = await bot.wait_for("message",check=check)
    
    if mes.content.lower() == text.lower():
        await ctx.send("<a:congratulation:1164962077052522677> Congratulations you have passed the captcha")
        role = ctx.guild.get_role(role_captcha_id)
        await ctx.author.add_roles(role)


if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            fmp = filename[:-3]
            bot.load_extension(f"cogs.{fmp}")
    bot.run(token)