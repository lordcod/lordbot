from typing import Any,Dict,Union
import psycopg2
import ujson as json
import threading
import asyncio
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
    print(err)

with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guilds (
            id INT8 PRIMARY KEY,
            forum_messages JSON DEFAULT '{}',
            reactions JSON DEFAULT '{}',
            auto_translate JSON DEFAULT '{}',
            language TEXT DEFAULT 'en',
            economy JSON DEFAULT '{}',
            economy_settings JSON
        )
    ''')


def get_info():
    query = """
        SELECT
            column_name,
            ordinal_position,
            data_type,
            column_default
        FROM
            information_schema.columns
        WHERE
            table_name = 'guilds';
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        
        info = cursor.fetchall()
        
        return info

colums = {info[0]:list(info[1:]) for info in get_info()}
colums_name = colums.keys()

class Json:
    def loads(data):
        try:
            data = json.loads(data)
            return data
        except:
            return data
    
    def dumps(data):
        try:
            data = json.dumps(data)
            return data
        except:
            return data

class Formating:
    def on_error(func):
        def wrapped(data: Dict[Any,Any]):
            try:
                result = func(data)
                return result
            except:
                return data
        return wrapped
    
    def loads(data: Dict[str,Any]):
        new_data = {}
        for key in data:
            if key.isdigit:
                new_data[int(key)] = data[key]
            else:
                new_data[key] = data[key]
    
    def dumps(data: Dict[Union[str,int],Any]):
        new_data = {}
        for key in data:
            
            if type(key) == int:
                new_data[str(key)] = data[key]
            else:
                new_data[key] = data[key]

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
    @classmethod
    def create_guild(cls,guild_id: int):
        cls.__init__(guild_id)
    
    def init(self) -> None:
        if not RequstsDB.get(self.guild_id):
            RequstsDB.insert(self.guild_id)
    
    def __init__(self,guild_id) -> None:
        self.guild_id = guild_id
        self.init()

    @property
    def data(self):
        gdb = RequstsDB.get(self.guild_id)
        gdb = dict(zip(colums_name,gdb))
        return gdb
    
    def get(self, service, default=None):
        data = RequstsDB.get_from_service(self.guild_id,service)
        data = data[0]
        data = Json.loads(data)
        data = Formating.loads(data)
        if data is None:
            return default
        return data
    
    def set(self, service, value):
        value = Json.dumps(value)
        RequstsDB.update(self.guild_id,service,value)
    
    def __getattribute__(self, __name: str) -> Any:
        return object.__getattribute__(self, __name)
    
    def __getattr__(self, item):
        return None
    
    def __setattr__(self, key, value):
        return object.__setattr__(self, key, value)

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