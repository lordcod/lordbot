import requests
import os
import dotenv

dotenv.load_dotenv()
token = 'MTEzNDE4Nzg5ODE2MjQwMTI5MQ.GuBRzW.C4DfoOcU8mMY0MrWETGZrdY1hlbQlnM78H__NY'

url = 'https://discord.com/api/v9/guilds/1260639264518180866/members-search'
data = {"or_query": {}, "and_query": {}, "limit": 250}
headers = {
    'Authorization': token
}
res = requests.post(url, json=data, headers=headers)
print(res)
print(res.json())
