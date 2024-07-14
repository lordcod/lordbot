import asyncio
import string
import random
import sqlite3
import threading
import time
from pyngrok import ngrok
from flask import Flask, request, jsonify, Response
from nacl.signing import VerifyKey
import os
from nacl.exceptions import BadSignatureError
from dotenv import load_dotenv
import requests
from typing import Optional
load_dotenv()

port = 5000
token = os.environ['dybfuo_token']


class Commands:
    def __init__(self,  token: str) -> None:
        self.token = token
        self.headers = {
            'Authorization': 'Bot '+token
        }

        application_info = self.get_application_info()
        self.verifi_key = application_info['verify_key']
        self.application_id = application_info['id']
        self.endpoint = application_info['interactions_endpoint_url']

    def get_application_info(self):
        res = requests.get('https://discord.com/api/v9/applications/@me', headers=self.headers)
        data = res.json()
        return data

    def edit_application(self, endpoint: str):
        res = requests.patch('https://discord.com/api/v9/applications/@me', headers=self.headers, json={
            'interactions_endpoint_url': endpoint
        })
        data = res.json()
        if res.ok:
            self.application_id = data['id']
            self.endpoint = data['interactions_endpoint_url']

    def get_cmds(self):
        res = requests.get(f'https://discord.com/api/v9/applications/{self.application_id}/commands', headers=self.headers)
        data = res.json()
        return data

    def clear_cmds(self, command_names: Optional[list] = None):
        data = self.get_cmds()
        for cmd_data in data:
            if command_names and cmd_data['name'] not in command_names:
                continue
            res = requests.delete(f'https://discord.com/api/v9/applications/{self.application_id}/commands/'+cmd_data['id'], headers=self.headers)
            if not res.ok:
                print(f"Failed delete {cmd_data['name']} ({cmd_data['id']})")

    def update(self, id: str, description: Optional[str] = None, description_ru: Optional[str] = None):
        data = {}
        if description:
            data["description"] = description
        if description_ru:
            data["description_localizations"] = {
                'ru': description_ru or description
            }
        requests.patch(f'https://discord.com/api/v9/applications/{self.application_id}/commands/'+id, headers=self.headers, json=data)

    def register(self, name: str, description: str, description_ru: Optional[str] = None):
        for cmd in self.get_cmds():
            if cmd['name'] == name:
                self.update(cmd['id'], description, description_ru)
                return
        requests.post(f'https://discord.com/api/v9/applications/{self.application_id}/commands', headers=self.headers, json={
            "name": name,
            "type": 1,
            "description": description,
            "description_localizations": {
                'ru': description_ru or description
            }
        })


class Users:
    @staticmethod
    def fetchvalue(query: str, params: tuple = ()):
        cursor = db.cursor()
        cursor.execute(query, params)
        data = cursor.fetchone()
        db.commit()

        if not data:
            return None
        return data[0]

    @staticmethod
    def update_table():
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                token TEXT PRIMARY KEY,
                token_time INTEGER,
                discord_id INTEGER,
                roblox_id INTEGER,
                promocodes TEXT
            )
            """)
        cursor.close()

    @staticmethod
    def insert(token: str, discord_id: int):
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (token, discord_id) VALUES (?, ?)", (token, discord_id))
        db.commit()

    @staticmethod
    def get_token(discord_id: int):
        cursor = db.cursor()
        cursor.execute("SELECT token FROM users WHERE discord_id = ?", (discord_id,))
        token = cursor.fetchone()
        if not token:
            return None
        return token[0]

    @staticmethod
    def get_or_create_token(discord_id: int):
        token = Users.get_token(discord_id)

        if token is None:
            token = ''.join([random.choice(string.hexdigits) for _ in range(6)])
            Users.insert(token, discord_id)

        return token

    def get_dis_from_rb(roblox_id: int):
        cursor = db.cursor()
        cursor.execute("SELECT discord_id FROM users WHERE roblox_id = ?", (roblox_id,))
        discord_id = cursor.fetchone()
        cursor.close()
        if not discord_id:
            return None
        return discord_id[0]

    @staticmethod
    def set_roblox_with_token(roblox_id: int, token: str):
        if discord_id := Users.get_dis_from_rb(roblox_id):
            return 0

        cursor = db.cursor()

        cursor.execute("SELECT discord_id FROM users WHERE token = ?", (token,))
        discord_id = cursor.fetchone()

        if not discord_id:
            return 1

        cursor.execute('UPDATE users SET roblox_id = ? WHERE token = ?', (roblox_id, token))

        db.commit()

        return discord_id[0]


app = Flask(__name__)
cmd = Commands(token)
db = sqlite3.connect('lordclassic.db', check_same_thread=False)


def authorize():
    signature = request.headers.get('x-signature-ed25519')
    timestamp = request.headers.get('x-signature-timestamp')

    verify_key = VerifyKey(bytes.fromhex(cmd.verifi_key))

    try:
        verify_key.verify(f'{timestamp}{request.data.decode()}'.encode(),
                          bytes.fromhex(signature))
    except BadSignatureError:
        return False
    else:
        return True


@app.route('/roblox-auth', methods=['GET'])
def roblox_auth_get():
    roblox_id = request.args.get('id')
    discord_id = Users.get_dis_from_rb(roblox_id)
    if discord_id is None:
        return Response('roblox account not found', 404)
    return Response(str(discord_id), 200)


@app.route('/roblox-auth', methods=['POST'])
def roblox_auth():
    roblox_id = request.json['id']
    token = request.json['token']
    discord_id = Users.set_roblox_with_token(roblox_id, token)
    if discord_id == 0:
        return Response('the account is already registered', 208)
    if discord_id == 1:
        return Response('token not found', 400)
    return Response(str(discord_id), 200)


@app.route('/', methods=['GET'])
def home():
    return 'Как ты суда попал?'


@app.route('/', methods=['POST'])
def my_command():
    if not authorize():
        return Response('invalid request signature', status=401)
    if request.json["type"] == 1:
        return jsonify({"type": 1})
    elif request.json["data"]["name"] == 'invite':
        invite_link = 'https://discord.com/oauth2/authorize?client_id=1095713975532007434'
        if request.json['locale'] == 'ru':
            text = f"[**Нажмите, чтобы добавить на свой сервер**]({invite_link})"
        else:
            text = f"[**Click to add to your server**]({invite_link})"
    elif request.json["data"]["name"] == 'promo':
        if request.json['locale'] == 'ru':
            text = "Здесь может появиться **промокод**, срок действия которого ограничен, так что успейте его получить"
        else:
            text = "A **promo code** may appear here and its limited use, so have time to pick it up"
    elif request.json["data"]["name"] == 'verifi':
        user_id = int(request.json['member']['user']['id'])
        code = Users.get_or_create_token(user_id)
        if request.json['locale'] == 'ru':
            text = f"Введите эту команду в игре: **/verify {code}**"
        else:
            text = f"Enter this command in the game: **/verify {code}**"
    else:
        if request.json['locale'] == 'ru':
            text = "Я не нашел эту команду в своей базе данных"
        else:
            text = "I did not find this command in my database"
    return jsonify({
        "type": 4,
        "data": {
            "content": text,
            "flags": 64
        }
    })


def _update_app(cmd, public_url):
    cmd.edit_application(public_url+'/')


if __name__ == '__main__':
    Users.update_table()
    public_url = ngrok.connect(str(port)).public_url
    print(public_url)
    timer = threading.Timer(5, _update_app, (cmd, public_url))
    timer.start()
    app.run(host='0.0.0.0', port=port)
