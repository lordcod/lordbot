
from typing import Generator, List
import requests
import vk_api
import vk_api.longpoll
import vkpymusic

token = 'vk1.a.pW91Q79Lvf66tV6JHMD5tInt3Uk6QAKKnFg7WYtk0MY0wbLNPMF7sF5mq87RCUhYCDxOxvP7-G4i2tVA87ksv-e-gMdBKIRjVrb8L8C2uaBzwCjV5xr4eJasXDiVPTVOwIQnEKY1_rSXCCcaHc-9rzQSPXe8OZLw4tr-MR3pZWIJeenucHDILpWzfl3L9CTiwvxDzRLR9Kk7HlECcAGp7Q'


class Post:
    def __init__(self, data: dict) -> None:
        self.inner_type = data['inner_type']
        self.can_edit = data['can_edit']
        self.author_id = data['created_by']
        self.can_delete = data['can_delete']
        self.donut = data['donut']
        self.comments = data['comments']
        self.with_ads = bool(data['marked_as_ads'])
        self.zoom_text = data['zoom_text']
        self.short_text_rate = data['short_text_rate']
        self.compact_attachments_before_cut = data['compact_attachments_before_cut']
        self.hash = data['hash']
        self.type = data['type']
        self.attachments = data['attachments']
        self.date = data['date']
        self.from_id = data['from_id']
        self.id = data['id']
        self.with_favorite = data['is_favorite']
        self.owner_id = data['owner_id']
        self.post_type = data['post_type']
        self.text = data['text']

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} text='{self.text}'>"


class VkLongPoll:
    BASE_URL = 'https://api.vk.com/method/'

    def __init__(
        self,
        token: str,
        version: str = '5.92'
    ) -> None:
        self.token = token
        self.version = version

    def get_method(
        self,
        method: str,
        data: dict
    ) -> dict:
        data.update({
            'v': self.version,
            'access_token': self.token,
        })
        r = requests.post(
            self.BASE_URL + method,
            data,
            headers={'Cookie': ''}
        )
        data = r.json()
        if 'error' in data:
            return
        return data['response']

    def update_longserver(self) -> None:
        r = self.get_method(
            'groups.getLongPollServer',
            {'group_id': '222485128'}
        )
        self.server = r['server']
        self.key = r['key']
        self.ts = r['ts']

    @property
    def longpoll_url(self) -> str:
        return f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25'

    def _parse_events(self, changes: dict):
        events = [
            Post(data['object'])
            for data in changes
            if data['type'] == 'wall_post_new'
        ]
        return events

    def listen(self) -> Generator[Post, None, None]:
        self.update_longserver()
        while True:
            responce = requests.get(self.longpoll_url, timeout=35)
            data = responce.json()

            if failed := data.get('failed'):
                if failed == 1:
                    self.ts = data['ts']
                elif failed in {2, 3}:
                    self.update_longserver()
                continue

            self.ts = data['ts']
            events = self._parse_events(data['updates'])
            yield from events


vk = VkLongPoll(token)

# for post in vk.listen():
#     print(post)
