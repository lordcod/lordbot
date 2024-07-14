import requests
import orjson

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxLCJpZCI6IjEwOTU3MTM5NzU1MzIwMDc0MzQiLCJpYXQiOjE3MTY1NzE0Mjh9.nM5rd6aMuEC9yAgCHt-BtYMjwww3I5p0qb7euPYuG7k'

with open("bot/languages/commands_data.json", "rb") as file:
    content = file.read()
    _commands = orjson.loads(content)
    commands = _commands["commands"]

commands_dbl = []
for cmd in commands:
    commands_dbl.append({
        'name': cmd['name'],
        'description': cmd['brief_descriptrion']['en'],
        'type': 1
    })

headers = {
    'Authorization': 'Bot '+token
}
res = requests.post(
    'https://discordbotlist.com/api/v1/bots/1095713975532007434/commands', json=commands_dbl, headers=headers)
print(res.json())
