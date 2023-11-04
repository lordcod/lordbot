import psycopg2
import ujson as json
import threading
import asyncio
import re


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
        SELECT
        	column_name,
        	ordinal_position,
        	data_type,
        	column_default
        FROM
        	information_schema.columns
        WHERE
        	table_name = 'guilds';
    ''')
    ret = cursor.fetchall()
    
    pattern = "'(.*)'::([a-zA-Z0-9]*)"
    req = ret[2][3]
    fm = re.fullmatch(pattern,req)
    print(fm.groups())


print("Finish")
connection.close()