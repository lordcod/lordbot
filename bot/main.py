import nextcord
from nextcord.ext import (commands,application_checks,tasks)
from nextcord.utils import (get,find,escape_markdown)
import googletrans,os

from bot.databases.db import GuildDateBases
from bot.misc import (utils,env)
from bot.resources import (info,languages,errors)
from bot.views import views

translator = googletrans.Translator()



def get_command_prefixs(bot: commands.Bot, msg: nextcord.Message):
    prefix = utils.get_prefix(msg.guild.id)
    return [prefix, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]

bot = commands.Bot(command_prefix=get_command_prefixs,intents=nextcord.Intents.all())

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
    guild_data = GuildDateBases(thread.guild.id)
    afm = guild_data.get('thread_messages',{})
    thread_data = afm.get(thread.parent_id,None)
    if not thread_data:
        return
    
    content = thread_data.get('content','')
    content = utils.generate_message(content)
    await thread.send(**content)

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
    
    guild_data = GuildDateBases(message.guild.id)
    reactions = guild_data.get('reactions',{})
    auto_translate = guild_data.get('auto_translate',{})
    lang = guild_data.get('language','en')
    
    invite_code = await utils.check_invite(message.content)
    
    if message.channel.id in reactions:
        for react in reactions[message.channel.id]:
            await message.add_reaction(react)
    
    if message.channel.id in auto_translate:
        result = translator.translate(message.content,dest=auto_translate[message.channel.id])
        if result.src != auto_translate:
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
            wh = await utils.get_webhook(message.channel,bot.user)
            
            embed = nextcord.Embed(
                title=f'{languages.invites.title[lang]} {invite.guild.name}',
                url=invite.url,
                color=0x3829df,
                description=f"### **{languages.invites.channel_type[invite.channel.type.value]}{escape_markdown(invite.channel.name)}**"
            )
            embed.set_author(
                name=invite.guild.name,
                icon_url=invite.guild.icon
            )
            nextcord.Member.display_name
            if hasattr(invite.inviter,'name'):
                embed.set_footer(
                    text=f'{languages.invites.footer[lang]} {invite.inviter.display_name}',
                    icon_url=invite.inviter.avatar
                )
            else:
                embed.set_footer(
                    text=languages.invites.custom_invite[lang],
                    icon_url=invite.guild.icon
                )
            
            await message.delete()
            await wh.send(username=message.author.global_name,avatar_url=message.author.avatar.url,embed=embed)
        except (nextcord.errors.NotFound,errors.ErrorTypeChannel):
            pass
    
    
    await bot.process_commands(message)


@bot.slash_command(
    name="activiti",
    description="Create an activity",
)
@application_checks.guild_only()
async def activiti(
    interaction:nextcord.Interaction,
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
) -> None:
    lang = GuildDateBases(interaction.guild_id).language
    activiti = utils.find(lambda a: a['label']==act,info.activities_list)
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

@bot.command()
@commands.has_permissions(manage_guild=True)
async def add_emoji(ctx: commands.Context, name):
    em = ctx.message.attachments[0]
    await ctx.guild.create_custom_emoji(name=name,image=em)

@bot.command(aliases=["set","setting"])
async def settings(ctx: commands.Context):
    view = nextcord.ui.View()
    view.add_item(views.SetDropdown())
    await ctx.send(view=view)

def start_bot():
    for filename in os.listdir("./bot/cogs"):
        if filename.endswith(".py") and not filename.startswith("__init__"):
            fmp = filename[:-3]
            bot.load_extension(f"bot.cogs.{fmp}")
    
    bot.run(env.token_lord_the_tester)