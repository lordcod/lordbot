from os import environ
from dotenv import load_dotenv
load_dotenv()


anprim_token = "MTE2Mzc0NzQxOTg2ODExOTA0MA.GA6nMN.oGDmsgTtQX-40ov51airPeziHflOg7Z2_XNSt0"

token_lord_cord = environ.get("lordcord_token")
token_lord_kind = environ.get("lordkind_token")
token_lord_classic = environ.get("lordclassic_token")


class Tokens:
    token = token_lord_kind
