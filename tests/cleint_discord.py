import json
import threading
import asyncio
import aiohttp
import requests
import time
import websocket


token = "NjM2ODI0OTk4MTIzNzk4NTMx.GcTtlO.noEQzXaHYNnnNa4xmvMwPTwczqXRCZvVSBz-SI"

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")


RECV = json.loads(ws.recv())
enabled = True
heartbeat_interval = RECV['d']['heartbeat_interval']
ws.send(json.dumps({"op": 2, "d": {"token": token, "properties": {
    "$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))

BASE_API = "https://discord.com/api/v9"


def add_reaction(channel_id: int, message_id: int, reaction: str):
    emoji = reaction.strip("<>")
    url = f"{BASE_API}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    headers = {"Authorization": token}
    requests.put(url=url, headers=headers)


def hearbeat_send():
    while enabled:
        try:
            print("Hearbeat send!", "Next step", heartbeat_interval/1000)
            ws.send(json.dumps({
                "op": 1,
                "d": None
            }))
            time.sleep(heartbeat_interval/1000)
        except Exception as err:
            print('Hearbeat ERROR', err)
    print('Stop')


th = threading.Thread(target=hearbeat_send)
th.start()

while True:
    try:
        data = json.loads(ws.recv())
        if data['t'] == "MESSAGE_CREATE" and data['d']['channel_id'] == "1179069504651796562":
            add_reaction(
                data['d']['channel_id'], data['d']['id'], "😣")
    except KeyboardInterrupt:
        print('KI')
        enabled = False
        th.join(heartbeat_interval/1000)
        print('SKI')
        break
    except Exception as err:
        pass

ws.close()


async def main():
    session = aiohttp.ClientSession()
    session.ws_connect


if __name__ == "__main__":
    asyncio.run(main())
