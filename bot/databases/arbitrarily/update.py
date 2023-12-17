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
value = """
{
    "operate": 1,
    "distribution":{
        "channel":{
            "permission":1,
            "values":[1179782301035536514]
        }
    }
}
"""

with connection.cursor() as cursor:
    cursor.execute(
        """
            UPDATE 
                guilds 
            SET 
                command_permissions = jsonb_set(command_permissions::jsonb, '{balance}', %s) 
            WHERE 
                id = %s
        """, 
        (value, guild_id, )
    )



print("Finish")
connection.close()