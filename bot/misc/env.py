from enum import StrEnum
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Tokens(StrEnum):
    token_anprim = environ.get("anprim_token")
    token_lordcord = environ.get("lordcord_token")
    token_lordkind = environ.get("lordkind_token")
    token_lordсlassic = environ.get("lordclassic_token")
    token = environ.get("discord_token")
