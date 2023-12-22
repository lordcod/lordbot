from . import economyHD,guildHD, commandHD, rolesHD


def GuildDateBasesInstance(conn):
    guildHD.connection = conn
    
    classification = guildHD.GuildDateBases
    
    return classification

def EconomyMembedDBInstance(conn):
    economyHD.connection = conn
    
    classification = economyHD.EconomyMembedDB
    
    return classification

def CommandDBInstance(conn):
    commandHD.connection = conn
    
    classification = commandHD.CommandDB
    
    return classification


def RolesDBInstance(conn):
    rolesHD.connection = conn
    
    classification = rolesHD.RoleDateBases
    
    return classification