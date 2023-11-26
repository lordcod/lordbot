import nextcord
from nextcord.ext import commands
from nextcord.utils import find

from bot import languages
from bot.databases.db import GuildDateBases
from bot.resources import info

from typing import Union, Dict, List

class help_lines:
    def __init__(self) -> None:
        self.line = ''
    
    def add_line(self,string):
        self.line = f'{self.line}{string}\n'
    
    def get(self):
        return self.line


category_names: List[str] = info.categories.keys()

all_commands: List[Dict[str,Union[List[str],bool,str]]]  = []
for comd_list in info.categories.values():
    for com in comd_list:
        all_commands.append(com) 


def check_category(categoryName: str):
    for cateName in category_names:
        if categoryName.lower() == cateName.lower():
            return info.categories[cateName]
    return False

def check_command(commandName: str) -> Union[Dict[str,Union[List[str],bool,str]],bool]:
    for command_data in all_commands:
        if commandName.lower() == command_data.get('name'):
            return command_data
        if commandName.lower() in command_data.get('aliases'):
            return command_data
    return False


def generate_embed_not_var(embed):
    for categ in info.categories:
        lines = help_lines()
        
        for com in info.categories[categ]:
            args = ' '.join(com.get('arguments'))
            text = f"{com.get('name')} {args}"
            lines.add_line(text)
        
        embed.add_field(
            name=categ,
            value=lines.get(),
            inline=False
        )
    return embed

def generate_embed_category(embed,name, category):
    lines = help_lines()
    for com in category:
        args = ' '.join(com.get('arguments'))
        text = f"{com.get('name')}({args}) - {com.get('brief_descriptrion')}"
        lines.add_line(text)
        
    embed.add_field(
        name=name,
        value=lines.get()
    )
    return embed

def generate_embed_commands(embed: nextcord.Embed, commnds: Dict[str,Union[List[str],bool,str]]):
    args = ' '.join(commnds.get('arguments'))
    aliases = ', '.join(commnds.get('aliases'))
    
    embed.description = 'Description of the command'
    
    embed.add_field(
        name='Command name',
        value=commnds.get('name'),
        inline=True
    )
    if aliases:
        embed.add_field(
            name='Command aliases',
            value=aliases,
            inline=True
        )
    
    if args:
        embed.add_field(
            name='Arguments',
            value=args,
            inline=False
        )
    
    embed.add_field(
        name='Descriptrion',
        value=commnds.get('descriptrion'),
        inline=False
    )
    
    
    return embed




class help(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context, catcom: str = None):
        gdb = GuildDateBases(ctx.guild.id)
        colour = gdb.get('color')
        
        embed = nextcord.Embed(
            title='Help',
            description='Help on bot commands',
            color=colour
        )
        embed.set_footer(text=info.footer)
        
        if not catcom:
            embed = generate_embed_not_var(embed)
        elif check_category(catcom):
            catdata = check_category(catcom)
            embed = generate_embed_category(embed, catcom, catdata)
        elif check_command(catcom):
            camdata = check_command(catcom)
            embed = generate_embed_commands(embed,camdata)
        else:
            embed.add_field(
                name='Command/Category not found',
                value='Try to call it something else or look at the general сommand'
            )
            embed.remove_footer()
        
        await ctx.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(help(bot))