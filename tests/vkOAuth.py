import flask
from flask import Flask, redirect, request
import requests
from test_vk_api import vk

app = Flask(__name__)
api_auth_url = 'https://oauth.vk.com/authorize'
client_id = '51922313'
scope = 'groups.manage'
redirect_uri = 'https://lordcord.fun/vk-callback'
display = 'wap'
version = '5.92'


@app.route('/')
def home():
    auth_url_template = f'{api_auth_url}?client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&display={display}&v={version}&response_type=token'
    return redirect(auth_url_template)


@app.route('/vk-callback')
def vk_callback():
    token = request.args.get('access_token')
    user_id = request.args.get('user_id')
    responce_url = "https://api.vk.com/method/groups.get?"
    data = {
        'access_token': token,
        'v': '5.101',
        'filter': 'admin',
        'extended': '1',
        'user_id': user_id
    }
    responce_url += '&'.join([f'{k}={v}' for k, v in data.items()])
    return redirect(responce_url)


if __name__ == '__main__':
    app.run()
