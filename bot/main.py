import nextcord
from nextcord.ext import (commands,application_checks,tasks)
from nextcord.utils import (get,find)

import asyncio,orjson,random,googletrans,datetime as dtt
import pickle,time,threading,os,aiohttp,io,re

from bot.databases.db import GuildDateBases
from bot.misc import (utils,env)
from bot.resources import (info,languages,errors)
from bot.views import buttons

translator = googletrans.Translator()

bot = commands.Bot(command_prefix=info.DEFAULT_PREFIX,intents=nextcord.Intents.all())

guilds = GuildDateBases({
    'default':{
        'auto_forum_messages' : {},
        'auto_reactions' : {},
        'auto_translate' : {},
        'language':'en'
    }
})

@bot.event
async def on_ready():
    print(f"The bot is registered as {bot.user}")

@bot.event
async def on_disconnect():
    print("Bot is disconnect")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    print(error)

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    print(f"[HANDLER][on_application_command_error][{interaction.application_command}]: {error}")
    print(interaction.id)

@bot.event
async def on_interaction(interaction:nextcord.Interaction):
    await bot.process_application_commands(interaction)

@bot.event
async def on_thread_create(thread:nextcord.Thread):
    guild_base = guilds(thread.guild.id)
    afm = guild_base.get_afm(thread.id)
    if not afm:
        return
    
    await thread.send(embed=nextcord.Embed(**afm))

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
    
    guild_base = guilds(message.guild.id)
    reacts = guild_base.get_ar(message.channel.id)
    
    trans_lang = guild_base.get_at(message.channel.id)
    lang = guilds(message.guild.id).get_lang()
    
    invite_code = await utils.check_invite(message.content)
    
    if reacts:
        for rea in reacts:
            await message.add_reaction(rea)
    
    if trans_lang:
        result = translator.translate(message.content,dest=trans_lang)
        if result.src != trans_lang:
            embed = nextcord.Embed(
                title="",
                description=f'### {result.text}',
                color=0xa17fe0
            )
            embed._fields = [
                {
                    'name':f'{languages.auto_translate.field_name_from[lang]} {googletrans.LANGUAGES[result.src]}',
                    'value':f'',
                    'inline':True
                },
                {
                    'name':f'{languages.auto_translate.field_name_to[lang]} {googletrans.LANGUAGES[result.dest]}',
                    'value':f'',
                    'inline':True
                },
            ]
            embed.set_footer(text='Performed with LordBot',icon_url=bot.user.avatar.url)
            await message.channel.send(embed=embed)
    
    if invite_code:
        try:
            invite = await bot.fetch_invite(invite_code)
            translate = languages.invites(invite)
            wh = await utils.get_webhook(message.channel)
            name = message.author.global_name if message.author.global_name and message.author.name == message.author.display_name else message.author.display_name
            guild_icon = invite.guild.icon.url if invite.guild.icon else None
            
            embed = nextcord.Embed(title=translate.title[lang],url=invite.url,
                                    color=0x3829df,description=translate.description)
            embed.set_author(name=invite.guild.name,
                            icon_url=guild_icon)
            if hasattr(invite.inviter,'name'):
                embed.set_footer(text=translate.footer[lang],icon_url=invite.inviter.avatar.url)
            else:
                embed.set_footer(text="Cistom Invite Link",icon_url=guild_icon)
            
            if translate.is_guild:
                embed.add_field(name="Основная информация",value=translate.field_guild[lang])
            
            await message.delete()
            await wh.send(username=name,avatar_url=message.author.avatar.url,embed=embed)
        except (nextcord.errors.NotFound,errors.ErrorTypeChannel):
            pass
    
    
    await bot.process_commands(message)


@bot.slash_command(
    name="activiti",
    description="Create an activity)",
)
@application_checks.guild_only()
async def activiti(interaction:nextcord.Interaction,
    voice:nextcord.VoiceChannel=nextcord.SlashOption(
        required=True,
        name="voice",
        description="Select the voice channel in which the activity will work!"
    ),
    act=nextcord.SlashOption(
        required=True,
        name="activiti",
        description="Select the activity you want to use!",
        choices=[activ['label'] for activ in info.activities_list],
    ),
):
    lang = guilds(interaction.guild_id).get_lang()
    activiti = utils.find(lambda a: a['label']==act,activities_list)
    try:
        inv = await voice.create_invite(
            target_type=nextcord.InviteTarget.embedded_application,
            target_application_id=activiti['id']
        )
    except:
        await interaction.response.send_message(content=languages.activiti.failed[lang])
        return
    view = nextcord.ui.View(timeout=None)
    view.add_item(nextcord.ui.Button(label="Activiti",emoji=languages.Emoji.roketa,url=inv.url))
    emb = nextcord.Embed(title=f"**{languages.activiti.embed_title[lang]}**",color=0xfff8dc,description=languages.activiti.embed_description[lang])
    emb._fields = [
        {'name':languages.activiti.fields_label[lang],'value':activiti['label'],'inline':True},
        {'name':languages.activiti.fields_max_user[lang],'value':activiti['max_user'],'inline':True},
    ]
    await interaction.response.send_message(embed=emb,view=view,ephemeral=True)


def start_bot():
    for filename in os.listdir("./bot/cogs"):
        if filename.endswith(".py") and not filename.startswith("__init__"):
            fmp = filename[:-3]
            bot.load_extension(f"bot.cogs.{fmp}")
    bot.run(env.Tokens.token)