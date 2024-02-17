import datetime
import requests
import time
from datetime import datetime


api = "https://api.music.yandex.net"
token = "y0_AgAAAAA8S1W0AAG8XgAAAAD4mKec0UmysdxcQWiI2pifxEomjDizPiw"

method = "GET"
url = f"{api}/users/1011570100/likes/tracks"
headers = {
    "accept": "application/json",
    "Authorization": f"OAuth {token}"
}
data = {}

responce = requests.request(
    method,
    url,
    headers=headers
)

print(responce.status_code)
yjsaon = responce.json()

for tra in yjsaon['result']['library']['tracks']:
    dt = datetime.fromisoformat(tra['timestamp']).strftime("%m-%d-%Y %H:%M:%S")
    print(tra['timestamp'])
    print((
        f"{int(time.time()-dt.timestamp())}\n"
        f"https://music.yandex.ru/album/{tra['albumId']}/track/{tra['id']}\n"
    ))

"""
Logins

res2 = requests.request(
    "GET",
    f"https://login.yandex.ru/info?oauth_token={token}&format=json"
)

print(res2.status_code)
print(res2.json())
"""
