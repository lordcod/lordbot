from _connection import connection
import orjson


guild_id = 1179069504186232852

with connection.cursor() as cursor:
    cursor.execute(
        "SELECT command_permissions FROM guilds WHERE id = %s", (guild_id,))

    val = cursor.fetchone()[0]

datas = {}
for cmname, values in val.items():
    new_perms = {}

    for name, perm in values['distribution'].items():
        new_dict = {}
        new_names = {
            'cooldown': 'cooldown',
            'role': 'allow-role',
            'channel': 'allow-channel',
        }

        if name == 'cooldown':
            new_dict = perm
        elif name == 'channels':
            new_dict['channels'] = perm.get('values')
        elif name == 'role':
            new_dict = perm.get('values')

        new_perms[new_names[name]] = new_dict

    datas[cmname] = {'distribution': new_perms}


with connection.cursor() as cursor:
    cursor.execute(
        "UPDATE guilds SET command_permissions = %s WHERE id = %s", (orjson.dumps(datas).decode(), guild_id,))


print("Finish")
connection.close()
