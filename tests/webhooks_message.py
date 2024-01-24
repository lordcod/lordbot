import aiohttp
import asyncio

users = {
    1:{
        'name':'pagisee',
        'avatar':'https://uprostim.com/wp-content/uploads/2021/02/image183-1-1.jpg'
    },
    2:{
        'name':'Kikiniy',
        'avatar':'https://sun6-23.userapi.com/s/v1/ig2/9EHNPWhJP7QKLeai9dAHRgHZ1NzBoLkLWwnUYnoY_RtF6fzC-yxtNxtBEq0ax-9uABDOv_85HMrEtZE2a42ZEZ3W.jpg?size=841x841&quality=96&crop=29,29,841,841&ava=1'
    },
    3:{
        'name':'argentym',
        'avatar':'https://sopranoclub.ru/images/memy-na-avu-275-memnyh-avatarok/file56760.jpeg'
    },
    4:{
        'name':'dung',
        'avatar':'https://sun6-20.userapi.com/s/v1/ig2/NleALYQ5Z07m0kKLeGuxwDHY3v2SyJiZ_fobvgJSI4cgm4MUMaMrSUIEGFyOCPl8MjFA0RqRGnSGNUlD1CKlidAL.jpg?size=694x694&quality=95&crop=9,0,694,694&ava=1'
    },
    5:{
        'name':'ibabok',
        'avatar':'https://cdn.discordapp.com/attachments/1025369229668651029/1199350177182515301/eafbec5d56bef1acc4293f7ad1f0a2ab.jpeg?ex=65c238e5&is=65afc3e5&hm=22252b1d60b53654921df0290171628122e776df77574bb994155cfc4384084b&'
    }
}

replicated = [
    [1, 'q'],
    [2, 'qq'],
    [3, 'Прив))'],
    [4, 'Даров'],
    [5, 'Хай!'],
    [1, 'Чел, дай скатать матешу'],
    [3, 'Чо задано по инглишу'],
    [2, 'Хз не смотрел'],
    [3, 'Лад забей го гамать'],
    [2, 'Рил го'],
    [5, 'Гайсы, какой некст урок'],
    [1, 'Литра вроде'],
    [5, 'Пруфы есть? Кинь скрин что литра некст'],
    [3, 'А есть чёт по общаге'],
    [1, 'Она не чекнет, чиль'],
    [4, 'Мне двойку поставили'],
    [2, 'Лол'],
    [1, 'Мда... Треш'],
    [3, 'Тогда го со сквадом в Раст на вайп залетим'],
    [4, 'Да не, эти олухи на меня обиделись я клатч в КС не затащил']
]


webhook_url = "https://discord.com/api/webhooks/1199348598639431710/8SL-p9cjW07FORSBmyDPa5t_LKwBzDR5zC_T4sxrGwjoyO1TouhVyD6QVUJKgKyDLXFh"


async def send_message(ses: aiohttp.ClientSession, content: str, nick: str, avatar: str):
    data = {
        "content": content,
        "username": nick,
        "avatar_url": avatar,
    }
    async with ses.post(webhook_url, data=data) as responce:
        pass

async def final_nessage(ses: aiohttp.ClientSession):
    data = {
        "username": "Welcomer",
        "avatar_url": "https://sketchub.in/storage/project_files/7101/7019393.png",
        "content": "*Галина Евгеньевна присоединилась к чату*"
    }
    async with ses.post(webhook_url, data=data) as responce:
        pass

async def main():
    await asyncio.sleep(5)
    async with aiohttp.ClientSession() as session:
        for rep in replicated:
            user = users[rep[0]]
            await send_message(session, rep[1], user['name'], user['avatar'])
            await asyncio.sleep(1)
        await final_nessage(session)
        await asyncio.sleep(1)
        await send_message(session, '-', 'Hello', 'https://sketchub.in/storage/project_files/7101/7019393.png')


asyncio.run(main())