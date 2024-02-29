import yandex_music
import os
from dotenv import load_dotenv
load_dotenv("C:/Users/2008d/git/lordbot/.env")

client = await yandex_music.ClientAsync(os.environ.get('yandex_api_token')).init()
client.