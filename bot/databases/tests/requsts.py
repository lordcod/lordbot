import psycopg2

import sys
sys.path.append(r"C:\Users\2008d\git\lordbot\bot\databases")

from config import (host, port, user, password, db_name)

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
    )
    connection.autocommit = True
except Exception as err:
    print(type(err))
    print(err)

data = """
{
    "1179069504651796562":{
            "type":"message",
            "dest":"ru",
            "whitelist":["ru"]
        }
    }
"""
guild_id = 1179069504186232852
with connection.cursor() as cursor:
    cursor.execute('UPDATE guilds SET auto_translate = %s WHERE id = %s',(data,guild_id))



print("Finish")
connection.close()