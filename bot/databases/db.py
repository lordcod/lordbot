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

def registrated_table():
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guilds (
                id INT8 PRIMARY KEY,
                forum_messages JSON DEFAULT '{}',
                reactions JSON DEFAULT '{}',
                auto_translate JSON DEFAULT '{}',
                language TEXT DEFAULT 'en',
                economic_settings JSON DEFAULT '{}'
            )
    ''')

    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS economic (
                guild_id INT8 NOT NULL,
                member_id INT8 NOT NULL,
                balance INT8 DEFAULT '0',
                bank INT8 DEFAULT '0',
                daily INT8 DEFAULT '0',
                weekly INT8 DEFAULT '0',
                monthly INT8 DEFAULT '0'
            )
        ''')


colums = {
    'guilds':{},
    'economic':{}
}

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
        
        colums['guilds'] = list(info)
    
    query = """
        SELECT
            column_name,
            ordinal_position,
            data_type,
            column_default
        FROM
            information_schema.columns
        WHERE
            table_name = 'economic';
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        
        info = cursor.fetchall()
        
        colums['economic'] = list(info)

registrated_table()
get_info()


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
    
    @on_error
    def loads(data: Dict[str,Any]):
        new_data = {}
        for key in data:
            value = data[key]
            if key.isdigit:
                new_data[int(key)] = value
            else:
                new_data[key] = value
    
    @on_error
    def dumps(data: Dict[Union[str,int],Any]):
        new_data = {}
        for key in data:
            
            if type(key) == int:
                new_data[str(key)] = data[key]
            else:
                new_data[key] = data[key]


class EconomyMembedDB:
    def get(guild_id,member_id):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM economic WHERE guild_id = %s AND member_id = %s', (guild_id,member_id))
            
            guild = cursor.fetchone()
            
            return guild
    
    def insert(guild_id,member_id):
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO economic (guild_id,member_id) VALUES (%s,%s)', (guild_id,member_id))
    
    def update(guild_id,member_id,arg,value):
        if not EconomyMembedDB.get(guild_id,member_id):
            EconomyMembedDB.insert(guild_id,member_id)
        
        with connection.cursor() as cursor:
            cursor.execute(f'UPDATE economic SET {arg} = %s WHERE guild_id = %s AND member_id = %s', (value, guild_id, member_id))
            
            connection.commit()
    
    def update_list(guild_id,member_id,args):
        for arg in args:
            value = args[arg]
            EconomyMembedDB.update(guild_id,member_id,arg,value)
    
    def delete(guild_id,member_id):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM economic WHERE guild_id = %s AND member_id = %s', (guild_id,member_id))
            
            connection.commit()
    
    def delete_guild(guild_id):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM economic WHERE guild_id = %s', (guild_id,))
            
            connection.commit()

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
    
    def __init__(self,guild_id) -> None:
        if not RequstsDB.get(guild_id):
            RequstsDB.insert(guild_id)
        self.guild_id = guild_id

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
    
    def __getattr__(self, item):
        return None


def db_forever():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        connection.close()
        loop.close()
        exit()

thread = threading.Thread(target=db_forever,name='DataBase')
thread.start()