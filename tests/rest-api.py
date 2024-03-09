import requests
import orjson

url = "https://discord.bots.gg/api/v1/bots/1095713975532007434/stats"
data = orjson.dumps({
    "shardCount": 2,
    "guildCount": 100
}).decode()
headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJhcGkiOnRydWUsImlkIjoiNjM2ODI0OTk4MTIzNzk4NTMxIiwiaWF0IjoxNzA5ODk5OTkwfQ.gB9RN5qb_VhH1pEkT-ZWI_6DVGGehqRHrTIZlIrJm04",
    "Content-Type": "application/json"
}

res = requests.post(url, data=data, headers=headers)
print(res.json())
