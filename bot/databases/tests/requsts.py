import psycopg2
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
    value = '["captcha"]'
    id = 1165681101294030898
    cursor.execute(f'''
        UPDATE guilds SET disabled_commands = '{value}' WHERE id = {id}
    ''')



print("Finish")
connection.close()