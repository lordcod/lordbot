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
            return self.base['default']['language']
