import nextcord
from typing import Union
from nextcord.ext import commands

class ErrorTypeChannel(Exception):
    pass

class OnlyTeamError(commands.CommandError):
    def __init__(self, author: Union[nextcord.Member,nextcord.User]) -> None:
        self.author: Union[nextcord.Member,nextcord.User] = author
        super().__init__("This command can only be used by the bot team")

class NotActivateEconomy(commands.CommandError):
    pass