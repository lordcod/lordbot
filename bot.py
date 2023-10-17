import nextcord
from nextcord.ext import (commands,application_checks,tasks)
from nextcord import utils
from nextcord.utils import get

import asyncio
import orjson
import random
import datetime as dtt
import pickle
import time
import threading
import sys
import os
from config import *
import requests
import io
import loggering
import recaptcha

logger = loggering.get_logger()

DEFAULT_PREFIX = '.'



bot = commands.Bot(command_prefix=DEFAULT_PREFIX,intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    logger.info(f"The bot is registered as {bot.user}")

@bot.command()
async def say(ctx:commands.Context, *, message: str=None):
    files = []
    for attach in ctx.message.attachments:
        data = io.BytesIO(await attach.read())
        files.append(nextcord.File(data, attach.filename))
    
    try:
        message = orjson.loads(message)
        
        embeds = []
        if "embeds" in message and type(message["embeds"]) == dict:
            for em in message["embeds"]:
                nextcord.Embed.from_dict(em)
        
        if "content" in message:
            content = message['content']
        else:
            content = None
        
        if "flags" in message:
            flag = nextcord.MessageFlags()
            flag.value = message["flags"]
        else:
            flag = None
        
        await ctx.send(content=content,embeds=embeds,files=files,flags=flag)
    except orjson.JSONDecodeError:
        await ctx.send(message,files=files)
    await ctx.message.delete()

@bot.event
async def on_disconnect():
    logger.info("Bot is disconnect")

# @bot.event
# async def on_error(event,*args, **kwargs):
#     logger.error(f"[HANDLER][on_error][{event}]: ARG:{args} KWARG:{kwargs}")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    logger.error(f"[HANDLER][on_command_error][{ctx.command.name}]: {error}")

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    logger.error(f"[HANDLER][on_application_command_error][{interaction.application_command}]: {error}")

forum_messages = {
    1162708314761740309 : {'title':'Привет друг!)','description':"""
    • Избегаем мета-вопросов
    • Если вопрос касается непосредственно твоего кода:
    > Опубликой полный вывод ошибки с терминала,
    > Фрагмент кода, на который эта ошибка ссылается! 
    • Объясни как можно подробней свою проблему.
                            """
    },
}
auto_reactions = {
    1160838344356413496:['✅','❌']
}
laung_table = {}

@bot.event
async def on_thread_create(thread:nextcord.Thread):
    if thread.parent.id not in forum_messages:
        return

    mes = forum_messages[thread.parent.id]
    await thread.send(embed=nextcord.Embed(**mes))

@bot.event
async def on_interaction(interaction:nextcord.Interaction):
    logger.debug(interaction.type)
    await bot.process_application_commands(interaction)

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
    await bot.process_commands(message)

async def fav_activiti(interaction: nextcord.Interaction, arg: str):
    list = {}
    for act in activities_list:
        if interaction.guild.premium_subscription_count >= act['boost_level']:
            list[act['label']]=str(act['id']) 
    if not arg:
        await interaction.response.send_autocomplete(list)
        return
    get_near = {}
    for act in list:
        if act.lower().startswith(arg.lower()):
            get_near[act]=list[act]
    await interaction.response.send_autocomplete(get_near)

@bot.slash_command(name="activiti")
async def activiti(interaction:nextcord.Interaction,
    voice:nextcord.VoiceChannel=nextcord.SlashOption(
        name="voice",),
    act=nextcord.SlashOption(
        name="activiti",
        autocomplete=True,
        autocomplete_callback=fav_activiti,),
):
    try:
        inv = await voice.create_invite(
            target_type=nextcord.InviteTarget.embedded_application,
            target_application_id=int(act)
        )
    except:
        await interaction.response.send_message(content="This activity is unavailable or does not work")
        return
    view = nextcord.ui.View(timeout=None)
    view.add_item(nextcord.ui.Button(label="Activiti",emoji="<:rocket:1154866304864497724>",url=inv.url))
    emb = nextcord.Embed(title="**Активность успешно создана!**",color=0xfff8dc,description="Однако некоторые виды активностей могут быть недоступны для вашего сервера, если уровень бустов не соответствует требованиям активности.")
    await interaction.response.send_message(embed=emb,view=view,ephemeral=True)

@bot.command()
async def captcha(ctx:commands.Context):
    data,text = recaptcha.generator(random.randint(3,7))
    logger.debug(f"Captcha text: {text}")
    image_file = nextcord.File(data,filename="cap.png",description="Captcha",spoiler=True)
    await ctx.send(file=image_file)
    for i in range(3,0,-1):
        def check(mes:nextcord.Message):
            return mes.channel==ctx.channel and mes.author==ctx.author
        mes:nextcord.Message = await bot.wait_for("message",check=check)
        if mes.content.lower() == text.lower():
            await ctx.send("Вы прошли капчу")
            await ctx.author.add_roles(ctx.guild.get_role(role_captcha_id))
            break
    else:
        await ctx.send(f"Вы не прошли captcha")

if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            fmp = filename[:-3]
            bot.load_extension(f"cogs.{fmp}")
    bot.run(token)