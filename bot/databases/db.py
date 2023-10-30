from typing import Literal
import sqlite3
import orjson




connection = sqlite3.connect('bot/databases/gdb.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS guilds (
        id INTEGER,
        forum_messages TEXT DEFAULT '{}',
        reactions TEXT DEFAULT '{}',
        auto_translate TEXT DEFAULT '{}',
        language TEXT DEFAULT 'en',
        PRIMARY KEY("id")
    )
''')
connection.commit()

table = (
    'id',
    'forum_messages',
    'reactions',
    'auto_translate',
    'language'
)


class RequstsDB:
    def get(guild_id):
        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM guilds WHERE id = ?', (guild_id,))
        guild = cursor.fetchone()
        
        connection.commit()
        if not guild:
            return None
        
        return dict(zip(table,guild))
    
    def insert(guild_id):
        cursor = connection.cursor()
        
        cursor.execute('INSERT INTO guilds (id) VALUES (?)', (guild_id,))
        
        connection.commit()
    
    def update(guild_id,arg,value):
        if not RequstsDB.get(guild_id):
            RequstsDB.insert(guild_id)
        
        cursor = connection.cursor()
        
        cursor.execute(f'UPDATE guilds SET {arg} = ? WHERE id = ?', (value, guild_id))
        
        connection.commit()
    
    def delete(guild_id):
        cursor = connection.cursor()
        
        cursor.execute('DELETE FROM guilds WHERE id = ?', (guild_id,))
        
        connection.commit()
    
    def drop_table():
        cursor = connection.cursor()
        
        cursor.execute('DROP TABLE guilds')
        
        connection.commit()
    
    def update_kwargs(guild_id,**kwargs):
        if not RequstsDB.get(guild_id):
            RequstsDB.insert(guild_id)
        
        for kw in kwargs:
            RequstsDB.update(guild_id,kw,kwargs[kw])


class GuildDateBases:
    def __init__(self,guild_id):
        self.guild_id = guild_id

    @property
    def guild(self):
        if not hasattr(self,'guild_id'):
            return None
        gdb = RequstsDB.get(self.guild_id)
        if not gdb:
            RequstsDB.insert(self.guild_id)
            gdb = RequstsDB.get(self.guild_id)
        return gdb
    
    def _get_atr_service(self, service):
        guild = self.guild
        if not guild:
            return None
        if not (service in guild and guild[service]):
            return None
        return guild[service]
    
    def _set_atr_service(self, service, value):
        RequstsDB.update(self.guild_id,service,value)
    
    @property
    def forum_messages(self):
        service = 'forum_messages'
        data = self._get_atr_service(service)
        data = orjson.loads(data)
        return data
    
    @property
    def reactions(self):
        service = 'reactions'
        data = self._get_atr_service(service)
        data = orjson.loads(data)
        return data
    
    @property
    def auto_translate(self):
        service = 'auto_translate'
        data = self._get_atr_service(service)
        data = orjson.loads(data)
        return data

    @property
    def language(self):
        service = 'language'
        data = self._get_atr_service(service)
        return data

    def set_forum_messages(self, value):
        service = 'forum_messages'
        self._set_atr_service(service,value)
    
    def set_reactions(self, value):
        service = 'reactions'
        self._set_atr_service(service,value)
    
    def set_auto_translate(self, value):
        service = 'auto_translate'
        self._set_atr_service(service,value)
    
    def set_language(self, value):
        service = 'language'
        self._set_atr_service(service,value)

