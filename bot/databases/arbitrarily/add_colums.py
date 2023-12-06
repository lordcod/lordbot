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


with connection.cursor() as cursor:
    query = """
        ALTER TABLE guilds
        ADD greeting_message JSON DEFAULT '{}'; 
    """
    cursor.execute(query)



print("Finish")
connection.close()