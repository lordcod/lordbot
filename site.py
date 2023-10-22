import flask
from flask import (Flask,redirect,session,render_template)
import string
import nextcord
import aiohttp
import logging
import time
import json

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

password = 'dv'#''.join(random.choice(string.ascii_letters + string.digits) for _ in range(26))
app.secret_key = password

lord = "http://localhost:5000"

api = 'https://discord.com/api/v10'
redirect_uri = f'{lord}/link-role-callback'
client_id = '1095713975532007434'
client_secret = 'Dq0HY3D3sAxauD2_HxEsIxzZoyBT5_4H'
scope = 'role_connections.write+guilds+identify+applications.commands.permissions.update'
url_auth = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
token = "MTA5NTcxMzk3NTUzMjAwNzQzNA.GdoeFJ.RuUbalItmQArVDmqcKLLK_2eImRpt-glwLyarI"



# ? OAuth2 discord
async def getOAuthTokens(code):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    } 
    headers={'Content-Type':'application/x-www-form-urlencoded'}
    url = f'{api}/oauth2/token'
    async with aiohttp.ClientSession() as session:
        res = await session.post(url,data=data,headers=headers)
        json = await res.json()
        return json

async def updateTokens(tokens):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'redirect_uri': redirect_uri
    }
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    url = f'{api}/oauth2/token'
    async with aiohttp.ClientSession() as session:
        res = await session.post(url,data=data,headers=headers)
        json = await res.json()
        return json

async def getUserDate(tokens):
    headers={"Authorization": "Bearer "+tokens['access_token']}
    url = f'{api}/users/@me'
    async with aiohttp.ClientSession() as session:
        res = await session.get(url,headers=headers)
        json = await res.json()
        return json

async def pushMetadate(metadata,tokens):
    data = metadata
    headers={
        'Authorization': 'Bearer '+tokens['access_token'],
        'Content-Type': 'application/json',
    }
    url = f'{api}/users/@me/applications/{client_id}/role-connection'
    async with aiohttp.ClientSession() as session:
        res = await session.post(url,data=data,headers=headers)
        json = await res.json()
        return json

async def getMetadata(tokens):
    headers= {
        'Authorization': 'Bearer '+tokens['access_token'],
        }
    url = f'{api}/users/@me/applications/{client_id}/role-connection'
    async with aiohttp.ClientSession() as session:
        res = await session.put(url,headers=headers)
        json = await res.json()
        return json

async def getGuilds(tokens):
    url = f'{api}/users/@me/guilds'
    params = {'limit':200}
    headers={"Authorization":f"Bearer {tokens['access_token']}",'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        res = await session.get(url,params=params,headers=headers)
        jsons = await res.json()
        return jsons

async def getGuildMember(guild_id,member_id):
    url=f'{api}/guilds/{guild_id}/members/{member_id}'
    headers={"Authorization": f'Bot {token}',"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        res = await session.get(url,headers=headers)
        json = await res.json()
        return json

async def isBotGuild(guild_id):
    res = await getGuildMember(guild_id,"1095713975532007434")
    if 'code' not in res:
        return True
    return False

async def addGuild(guild_id,user_id,tokens):
    url=f'{api}/guilds/{guild_id}/members/{user_id}',
    data=json.dumps({'access_token':tokens['access_token']}),
    headers={"Authorization": f'Bot {token}',"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        res = await session.put(url,data=data,headers=headers)
        json = await res.json()
        return json

async def editPermissionCommand(guild_id,command_id,value,tokens):
    url = f'{api}/applications/{client_id}/guilds/{guild_id}/commands/{guild_id}/permissions'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization":f"Bearer {tokens['access_token']}"
    }   
    data = {
        'permissions':[
            {'id': guild_id, 'type': 1, 'permission': value}
        ]
    }
    async with aiohttp.ClientSession() as session:
        res = await session.put(url,data=json.dumps(data),headers=headers)
        print(await res.json())


@app.route("/link-role-callback")
async def role_callback():
    code = flask.request.args.get('code')
    if code:
        tokens = await getOAuthTokens(code)
        if 'error' in tokens:
            return tokens['error']
        tokens['expires_in'] += time.time()
        session['tokens'] = tokens
        return redirect("/")
    else:
        return "Error no attribyte code"

@app.route("/")
async def home():
    if 'tokens' not in session:
        return redirect(url_auth)

    tokens = session['tokens']
    if time.time() >= tokens['expires_in']:
        tokens = await updateTokens(tokens)
        tokens['expires_in'] += time.time()
        session['tokens'] = tokens
    user = await getUserDate(tokens)
    if 'code' in user:
        del session['tokens']
        return redirect(url_auth)
    
    
    return '1'

if __name__ == "__main__":
    app.run("0.0.0.0")