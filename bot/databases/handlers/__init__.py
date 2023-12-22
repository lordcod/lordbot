from . import economyHD,guildHD, commandHD


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