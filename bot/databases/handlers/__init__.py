from . import guildHD, economyHD, commandHD, rolesHD, mongoHD, bansHD

from .guildHD import GuildDateBases
from .economyHD import EconomyMembedDB
from .commandHD import CommandDB
from .rolesHD import RoleDateBases
from .bansHD import BanDateBases
from .mongoHD import MongoDB


def establish_connection(conn):
    guildHD.connection = conn
    economyHD.connection = conn
    commandHD.connection = conn
    rolesHD.connection = conn
    bansHD.connection = conn
    mongoHD.connection = conn
