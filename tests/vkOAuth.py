import flask
from flask import Flask, redirect, render_template, request
import requests
from test_vk_api import vk

app = Flask(__name__)
api_auth_url = 'https://oauth.vk.com/authorize'
client_id = '51922313'
scope = 'groups.manage'
redirect_uri = 'https://lordcord.fun/vk-callback'
display = 'wap'
version = '5.92'
localhost = "http://localhost:5000/"


@app.route('/')
def home():
    auth_url_template = f'{api_auth_url}?client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&display={display}&v={version}&response_type=token'
    return redirect(auth_url_template)


@app.route('/test')
def test():
    return render_template('index.html')


@app.route('/vk-callback')
def vk_callback():
    token = request.args.get('access_token')
    user_id = request.args.get('user_id')
    return render_template('index.html', token=token, user_id=user_id)


if __name__ == '__main__':
    app.run()
