import os
from typing import Optional
from pprint import pprint
import nextcord
import requests
from dotenv import load_dotenv
load_dotenv()


flags = nextcord.MessageFlags()
flags.ephemeral = True

nextcord.Locale.ru

application_id = 1260581113529766040
token = os.environ['dybfuo_token']


class Commands():
    def __init__(self, application_id, token) -> None:

        self.application_id = application_id
        self.headers = {
            'Authorization': 'Bot '+token
        }

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
        res = requests.patch(f'https://discord.com/api/v9/applications/{self.application_id}/commands/'+id, headers=self.headers, json=data)
        pprint(res.json())

    def register(self, name: str, description: str, description_ru: Optional[str] = None):
        for cmd in self.get_cmds():
            if cmd['name'] == name:
                self.update(cmd['id'], description, description_ru)
                return
        res = requests.post(f'https://discord.com/api/v9/applications/{self.application_id}/commands', headers=self.headers, json={
            "name": name,
            "type": 1,
            "description": description,
            "description_localizations": {
                'ru': description_ru or description
            }
        })
        pprint(res.json())


if __name__ == '__main__':
    cmd = Commands(application_id, token)
    cmd.register(
        'invite',
        'Invite the bot to your server',
        'Пригласи бота на свой сервер'
    )
    cmd.register(
        'promo',
        'Get a promo code',
        'Получи промо-код'
    )
    cmd.register(
        'verifi',
        'Go through verification and link your account to roblox and you will also find a sweet one',
        'Пройдите верификацию и привяжите свой аккаунт к roblox, и вы тоже найдете что-то интересное'
    )
