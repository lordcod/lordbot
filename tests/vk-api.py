from pprint import pprint
import re
import requests
from vkaudiotoken import get_kate_token, get_vk_official_token

kt_access_token = "vk1.a.11pGsKeKMJEsNQL2szPcyY7MXX0Uqd5wqTL5wxbv47fbCJziLR7ORWGrxQ2l84JC-0v0kGzdOMzbIn5VHM15Se3E9U6pbXkCZxA_rBNuVTAIZpQivsjtsUvIgWAAHWcT91bDHXHEBVs4zJlIOj-nE0FTwqw4vMno0mIlyQylGQwHaik5N9PjmclxdffE8Er5vdcf7C1XtebqvdA6f8ALEQ"
kt_user_agent = "KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)"
of_access_token = "vk1.a.WldeAkLpl_r-YiT2j5NCvkXghgl5Ss7UEQd51jL8Aify3AhyHGplDDlhfWQ2pTKY3Q5iN7tlGFjQwh92CaW_qdacdAZ6UHwx-_PwEaDUsjZTrWo_Uu-ta-FToEJACTmJv7YNVcWabLT6HzuVLajVGMn-cm4-tWpKRd0UtHTTeS4FGjyGF-T9BHSeyv3yW2mw"
of_user_agent = "VKAndroidApp/5.52-4543 (Android 5.1.1; SDK 22; x86_64; unknown Android SDK built for x86_64; en; 320x240)"

# login = "+79999269010"
# password = "889900dddd"

# print(get_kate_token(login, password))
# print(get_vk_official_token(login, password))

# TODO Regex


def get_audio_id_by_link(link: str):
    if data := re.fullmatch(r"https://vk.com/audio([0-9-_]+)", link):
        return data.group(1)


# TODO Search
data = {
    "access_token": kt_access_token,
    "https": 1,
    "lang": "en",
    "extended": 1,
    "v": 5.131,
    "q": "Поболело и прошло"
}
headers = {"User-Agent": kt_user_agent}

responce = requests.post(
    "https://api.vk.com/method/audio.search",
    data,
    headers=headers
)


# TODO GetById

track_id = get_audio_id_by_link(input(">"))
data = {
    "access_token": kt_access_token,
    "https": 1,
    "lang": "en",
    "extended": 1,
    "v": 5.131,
    "audios": [track_id]
}
headers = {"User-Agent": kt_user_agent}

responce = requests.post(
    "https://api.vk.com/method/audio.getById",
    data,
    headers=headers
)
pprint(responce.json())
