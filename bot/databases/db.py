from typing import Any
import psycopg2
import ujson as json
import threading
import asyncio


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
            id INT8 PRIMARY KEY,
            forum_messages BYTEA DEFAULT '{}',
            reactions BYTEA DEFAULT '{}',
            auto_translate BYTEA DEFAULT '{}',
            language TEXT DEFAULT 'en'
        )
    ''')

def encode(data):
    try:
        data = json.dumps(data)
    except:
        pass
    return data

def decode(data):
    new_data = {}
    for d in data:
        try:
            dejson = json.loads(data[d])
            new_data[d] = dejson
        except:
            new_data[d] = data[d]
    return new_data


def get_info():
    query = """
        SELECT
            column_name,
            ordinal_position,
            data_type
        FROM
            information_schema.columns
        WHERE
            table_name = 'guilds';
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        
        info = cursor.fetchall()
        
        if not info:
            return None
        return info

colums = [info[0] for info in get_info()]


class RequstsDB:
    def get(guild_id):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM guilds WHERE id = %s', (guild_id,))
            
            guild = cursor.fetchone()
            
            return guild
    
    def get_from_service(guild_id,arg):
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT {arg} FROM guilds WHERE id = %s', (guild_id,))
            
            value = cursor.fetchone()
            
            return value
    
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
    
    def update_from_kwargs(guild_id,**kwargs):
        if not RequstsDB.get(guild_id):
            RequstsDB.insert(guild_id)
        
        for kw in kwargs:
            RequstsDB.update(guild_id,kw,kwargs[kw])
    
    def delete(guild_id):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM guilds WHERE id = %s', (guild_id,))
            
            connection.commit()
    
    def drop_table():
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE guilds')
            
            connection.commit()


class GuildDateBases:
    def init(self) -> None:
        if not RequstsDB.get(self.guild_id):
            RequstsDB.insert(self.guild_id)
    
    def __init__(self,guild_id) -> None:
        self.guild_id = guild_id
        self.init()

    @property
    def data(self):
        gdb = RequstsDB.get(self.guild_id)
        gdb = dict(zip(colums,gdb))
        gdb = decode(gdb)
        return gdb
    
    def _get_data(self, service, default=None):
        data = RequstsDB.get_from_service(self.guild_id,service)
        if data is None or data[0] is None:
            return default
        return data[0]
    
    def _set_data(self, service, value):
        RequstsDB.update(self.guild_id,service,value)
    
    def __getattribute__(self, __name: str) -> Any:
        if __name == '':
            return None
        if __name in colums:
            data = self._get_data(__name)
            return data
        else:
            return object.__getattribute__(self, __name)
    
    def __getattr__(self, item):
        return None
    
    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

def db_forever():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        connection.close()
        loop.close()

thread = threading.Thread(target=db_forever,name='DataBase')
thread.start()