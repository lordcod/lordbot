import psycopg2

host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
user = 'j5191558_cord'
password = 'fd5-DVv-pf5-6bx'
db_name = 'j5191558_main'





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
data = '{"1175404400215326802":["🟢","🔴"]}'
with connection.cursor() as cursor:
    cursor.execute('UPDATE guilds SET reactions = %s WHERE id = %s',(data,1171849727210426459))



print("Finish")
connection.close()