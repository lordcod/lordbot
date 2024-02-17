from _connection import connection


guild_id = 1179069504186232852

with connection.cursor() as cursor:
    cursor.execute(
        "SELECT command_permissions ->> 'pay' FROM guilds WHERE id = %s", (guild_id,))

    val = cursor.fetchone()
    print(val)
    print(val[0])


print("Finish")
connection.close()
