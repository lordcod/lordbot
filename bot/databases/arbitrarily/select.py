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


guild_id = 1179069504186232852

with connection.cursor() as cursor:
    cursor.execute("SELECT command_permissions ->> 'ping' FROM guilds WHERE id = %s",(guild_id,))
    
    val = cursor.fetchone()
    print(val)
    print(val[0])



print("Finish")
connection.close()