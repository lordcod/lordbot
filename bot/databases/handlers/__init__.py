from . import economyHD,guildHD


def GuildDateBasesInstance(conn):
    guildHD.connection = conn
    
    classification = guildHD.GuildDateBases
    
    return classification

def EconomyMembedDBInstance(conn):
    economyHD.connection = conn
    
    classification = economyHD.EconomyMembedDB
    
    return classification
