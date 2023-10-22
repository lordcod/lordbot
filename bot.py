import nextcord
from nextcord.ext import (commands,application_checks,tasks)
from nextcord import utils
from nextcord.utils import get,find

import asyncio,orjson,random,googletrans,datetime as dtt,\
pickle,time,threading,os,aiohttp,io,recaptcha,languages
from config import *

translator = googletrans.Translator()

DEFAULT_PREFIX = 'l.'

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

class GuildDateBases:
    def __init__(self,base:dict):
        self.base = base

    def __call__(self,guild_id):
        self.guild_id = guild_id
        self.get_guild(guild_id)
        return self 

    def get_guild(self,guild_id):
        if guild_id in self.base:
            return self.base[guild_id]
        else:
            self.base[guild_id] = {}
            return self.base[guild_id]
    
    def get_afm(self,channel_id):
        if not self.guild_id:
            return None
        service = 'auto_forum_messages'
        if service in self.base[self.guild_id] and channel_id in self.base[self.guild_id][service]:
            return self.base[self.guild_id][service][channel_id]
        else:
            return False
    
    def get_ar(self,channel_id):
        if not self.guild_id:
            return None
        service = 'auto_reactions'
        if service in self.base[self.guild_id] and channel_id in self.base[self.guild_id][service]:
            return self.base[self.guild_id][service][channel_id]
        else:
            return False
    
    def get_at(self,channel_id):
        if not self.guild_id:
            return None
        service = 'auto_translate'
        if service in self.base[self.guild_id] and channel_id in self.base[self.guild_id][service]:
            return self.base[self.guild_id][service][channel_id]
        else:
            return False

    def get_lang(self):
        if not self.guild_id:
            return None
        if 'language' in self.base[self.guild_id]:
            return self.base[self.guild_id]['language']
        else:
            return 'ru'

guilds = GuildDateBases({
    'exemple':{
        'auto_forum_messages' : {
            'channel_id':{'embed'}
        },
        'auto_reactions' : {
            'channel_id':['reaction']
        },
        'auto_translate' : {
            'channel_id':'laung',
        },
        'language':'en'
    },
    1095713596790550589:{
        'auto_reactions' : {
            1095713596790550592:['<:pwease:1163469696717291671>'],
        },
        'auto_translate' : {},
        'language':'ru'
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
    print(f"[HANDLER][on_command_error][{ctx.command.name}]: {error}")

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    print(f"[HANDLER][on_application_command_error][{interaction.application_command}]: {error}")
    print(interaction.id)


@bot.event
async def on_interaction(interaction:nextcord.Interaction):
    print(interaction.type)
    await bot.process_application_commands(interaction)

@bot.event
async def on_thread_create(thread:nextcord.Thread):
    guild_base = guilds(message.guild.id)
    emb = guild_base.get_afm(thread.id)
    if not emb:
        return
    
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
    
    guild_base = guilds(message.guild.id)
    reacts = guild_base.get_ar(message.channel.id)
    trans_lang = guild_base.get_at(message.channel.id)
    lang = guilds(message.guild.id).get_lang()
    
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
        choices=[activ['label'] for activ in activities_list],
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
    view.add_item(nextcord.ui.Button(label="Activiti",emoji="<:rocket:1154866304864497724>",url=inv.url))
    emb = nextcord.Embed(title=f"**{languages.activiti.embed_title[lang]}**",color=0xfff8dc,description=languages.activiti.embed_description[lang])
    emb._fields = [
        {'name':languages.activiti.fields_label[lang],'value':activiti['label'],'inline':True},
        {'name':languages.activiti.fields_max_user[lang],'value':activiti['max_user'],'inline':True},
    ]
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
    lang = guilds(ctx.guild.id).get_lang()
    data,text = recaptcha.generator(random.randint(3,7))
    image_file = nextcord.File(data,filename="cap.png",description="Captcha",spoiler=True)
    await ctx.send(content=languages.captcha.enter[lang],file=image_file)
    try:
        check = lambda m: m.channel==ctx.channel and m.author==ctx.author
        mes:nextcord.Message = await bot.wait_for("message",timeout=30,check=check)
    except asyncio.TimeoutError:
        await ctx.send(content=languages.captcha.failed[lang])
        return
    
    if mes.content.lower() == text.lower():
        await ctx.send(f"<a:congratulation:1164962077052522677>{languages.captcha.congratulation[lang]}")
        role = ctx.guild.get_role(role_captcha_id)
        await ctx.author.add_roles(role)
    else:
        await ctx.send(content=languages.captcha.failed[lang])


if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            fmp = filename[:-3]
            bot.load_extension(f"cogs.{fmp}")
    bot.run(token)