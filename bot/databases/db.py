import psycopg2
import orjson


host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
password = 'nVR*6#1P%hyR*4l0'
user = 'j5191558_bot'
db_name = 'j5191558_main'


try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
except Exception as err:
    print(type(err))
    print(err)

with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guilds (
            id INTEGER PRIMARY KEY,
            forum_messages BYTEA DEFAULT '{}',
            reactions BYTEA DEFAULT '{}',
            auto_translate BYTEA DEFAULT '{}',
            language TEXT DEFAULT 'en'
        )
    ''')

def decode(data):
    new_data = {}
    for d in data:
        try:
            dejson = orjson.loads(data[d])
            new_data[d] = dejson
        except:
            new_data[d] = data[d]
    return new_data

table = (
    'id',
    'forum_messages',
    'reactions',
    'auto_translate',
    'language'
)

class RequstsDB:
    def get(guild_id):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM guilds WHERE id = %s', (guild_id,))
            
            guild = cursor.fetchone()
            
            if not guild:
                return None
            return guild
    
    def insert(guild_id):
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO guilds (id) VALUES (%s)', (guild_id,))
            
            connection.commit()
    
    def update(guild_id,arg,value):
        if not RequstsDB.get(guild_id):
            RequstsDB.insert(guild_id)
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE guilds SET {arg} = %s WHERE id = %s', (value, guild_id))
            
            connection.commit()
    
    def delete(guild_id):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM guilds WHERE id = %s', (guild_id,))
            
            connection.commit()
    
    def drop_table():
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE guilds')
            
            connection.commit()
    
    def update_from_kwargs(guild_id,**kwargs):
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
        
        gdb = dict(zip(table,gdb))
        gdb = decode(gdb)
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


connection.close()
