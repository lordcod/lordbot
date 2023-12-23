import nextcord
from nextcord.ext import commands

from bot.misc.ratelimit import Cooldown
from bot.misc.logger import Logger
from bot.resources import errors
from bot.databases.db import GuildDateBases, CommandDB
from bot.resources.errors import CallbackCommandError, MissingRole, MissingChannel, CommandOnCooldown

TrueType = type(True)
NumberType = (int, float)

class PermissionChecker:
    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx
    
    async def process(self) -> bool:
        ctx = self.ctx
        command_name = ctx.command.qualified_name
        cdb = CommandDB(ctx.guild.id)
        self.command_permissions = cdb.get(command_name, {})
        
        enabled = await self.is_enabled()
        allowed = await self.is_allowed()
        
        answer = enabled & allowed
        return answer
    
    async def is_enabled(self):
        "Checks whether it is enabled"
        command_permissions = self.command_permissions
        operate = command_permissions.get("operate",1)
        
        if operate == 0:
            raise errors.DisabledCommand()
        return True
    
    async def is_allowed(self):
        "Checks if there are permissions to use the command"
        command_permissions = self.command_permissions
        distribution: dict = command_permissions.get("distribution",{})
        
        for type, data in distribution.items():
            meaning = self.allowed_types[type]
            value = await meaning(self, data)
            if not value:
                return False
        return True
    
    async def _is_allowed_role(self, data: dict) -> bool:
        "The `is_allowed` subsection is needed to verify roles"
        ctx = self.ctx
        author = ctx.author
        aut_roles_ids = author._roles
        perm_roles_ids = data.get("values",[])
        
        if not perm_roles_ids:
            return True
        
        common = set(perm_roles_ids) & set(aut_roles_ids)
        if not common:
            raise MissingRole()
        return True
    
    async def _is_allowed_channel(self, data: dict) -> bool:
        "The `is_allowed` subsection is needed to verify channels"
        ctx = self.ctx
        channel = ctx.channel
        channels_ids = data.get("values",[])
        
        if channel.id not in channels_ids:
            raise MissingChannel()
        return True
    
    async def _is_allowed_cooldown(self, data: dict) -> bool:
        ctx = self.ctx
        cooldown = Cooldown(
            ctx.command.qualified_name,
            data,
            ctx.guild.id,
            ctx.author.id
        )
        retry = cooldown.get()
        cooldown.add()
        
        if isinstance(retry,TrueType):
            return True
        elif isinstance(retry, NumberType):
            raise CommandOnCooldown(retry)
        else:  
            raise TypeError()
    
    allowed_types = {
        'role':_is_allowed_role,
        'channel':_is_allowed_channel,
        'cooldown':_is_allowed_cooldown
    }

class command_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        
        # bot.event(self.on_error)
        bot.event(self.on_command_error)
        bot.event(self.on_application_error)
        
        bot.add_check(self.permission_check)
    
    async def on_application_error(self, interaction, error):
        pass
    
    async def on_command_error(self, ctx: commands.Context, error):
        CommandError = CallbackCommandError(ctx,error)
        await CommandError.process()
    
    async def on_error(self, event, *args,**kwargs):
        Logger.error(event)
    
    async def permission_check(self,  ctx: commands.Context):
        perch = PermissionChecker(ctx)
        answer = await perch.process()
        
        return answer
    




def setup(bot: commands.Bot):
    event = command_event(bot)
    
    bot.add_cog(event)