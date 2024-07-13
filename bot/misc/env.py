from os import environ
from dotenv import load_dotenv
load_dotenv()


class Tokens:
    token_anprim = environ.get("anprim_token")
    token_lord_cord = environ.get("lordcord_token")
    token_lord_kind = environ.get("lordkind_token")
    token_lord_classic = environ.get("lordclassic_token")
    token = token_lord_kind
    print(token_lord_cord)
