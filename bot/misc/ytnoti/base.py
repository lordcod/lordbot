import hmac
from http import HTTPStatus
from pyexpat import ExpatError
from uvicorn import Config, Server
from pyngrok import ngrok
import asyncio
import xmltodict
from fastapi import FastAPI, APIRouter, Request, Response
from ytypes import Channel, Thumbnail, Stats, Timestamp, Video, VideoHistory
from datetime import datetime
from httpx import AsyncClient


class YoutubeNotifier:
    endpoint: str
    password: str
    callback_url: str
    app: FastAPI
    _video_history: VideoHistory
    _subscribed_ids: list[str]

    def __init__(self) -> None:
        self._subscribed_ids = []
        self.add_subscribed = self._subscribed_ids.append
        self._video_history = VideoHistory()

    async def register_subscribed(self, channel_id: str):
        self.add_subscribed(channel_id)
        await self._register(channel_id)

    async def on_ready(self):
        tasks = []
        for cid in self._subscribed_ids:
            tasks.append(self._register(cid))
        await asyncio.gather(*tasks)

    async def on_video(self, video: Video):
        print(video)

    async def run(self,
                  *,
                  endpoint: str = '/',
                  port: int = 8000) -> None:
        server = self._setup(endpoint=endpoint, port=port)
        try:
            server.config.setup_event_loop()
            await server.serve()
        except KeyboardInterrupt:
            await server.shutdown()

    def _setup(self, endpoint: str, port: int):
        self.endpoint = endpoint
        self.password = 'secret-key'
        self.app = FastAPI()
        self.callback_url = ngrok.connect(str(port)).public_url
        self.app.include_router(self._get_router())
        self.app.add_event_handler("startup", lambda: asyncio.create_task(self.on_ready()))

        print(self.callback_url)

        config = Config(self.app, "0.0.0.0", port)
        server = Server(config)
        return server

    async def _publish(self, channel_id: str):
        async with AsyncClient() as client:
            await client.post(
                "https://pubsubhubbub.appspot.com",
                data={
                    "hub.mode": 'publish',
                    "hub.url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
                },
                headers={"Content-type": "application/x-www-form-urlencoded"}
            )

    async def _register(self, channel_id: str):
        async with AsyncClient() as client:
            res = await client.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
            body = xmltodict.parse(res.read().decode())
            for video in self.get_videos_from_body(body):
                if self._video_history.has(video):
                    continue
                self._video_history.add(video)

            await client.post(
                "https://pubsubhubbub.appspot.com",
                data={
                    "hub.mode": 'subscribe',
                    "hub.topic": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
                    "hub.callback": self.callback_url,
                    "hub.verify": "sync",
                    "hub.secret": self.password,
                    "hub.lease_seconds": "",
                    "hub.verify_token": ""
                },
                headers={"Content-type": "application/x-www-form-urlencoded"}
            )

    def _get_router(self) -> APIRouter:
        router = APIRouter()
        router.add_api_route(self.endpoint, self._get, methods=["HEAD", "GET"])
        router.add_api_route(self.endpoint, self._post, methods=["POST"])

        return router

    def get_videos_from_body(self, body: dict):
        videos = []
        entries = body["feed"]["entry"] if isinstance(body["feed"]["entry"], list) else [body["feed"]["entry"]]

        for entry in entries:
            channel = Channel(
                id=entry["yt:channelId"],
                name=entry["author"]["name"],
                url=entry["author"]["uri"],
                created_at=datetime.strptime(body["feed"]["published"], "%Y-%m-%dT%H:%M:%S%z")
            )

            thumbnail = Thumbnail(
                url=entry["media:group"]["media:thumbnail"]["@url"],
                width=int(entry["media:group"]["media:thumbnail"]["@width"]),
                height=int(entry["media:group"]["media:thumbnail"]["@height"]),
            )

            stats = None
            if "media:community" in entry["media:group"]:
                stats = Stats(
                    likes=int(entry["media:group"]["media:community"]["media:starRating"]["@count"]),
                    views=int(entry["media:group"]["media:community"]["media:statistics"]["@views"]),
                )

            timestamp = Timestamp(
                published=datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%S%z"),
                updated=datetime.strptime(entry["updated"], "%Y-%m-%dT%H:%M:%S%z")
            )

            videos.append(Video(
                id=entry["yt:videoId"],
                title=entry["title"],
                description=entry["media:group"]["media:description"] or "",
                url=entry["link"]["@href"],
                thumbnail=thumbnail,
                stats=stats,
                timestamp=timestamp,
                channel=channel
            ))

        return videos

    @staticmethod
    async def _get(request: Request):
        challenge = request.query_params.get("hub.challenge")
        if challenge is None:
            return Response(status_code=HTTPStatus.BAD_REQUEST.value)

        return Response(challenge)

    async def _post(self, request: Request):
        if not await self._is_authorized(request):
            return Response(status_code=HTTPStatus.UNAUTHORIZED.value)

        try:
            body = xmltodict.parse((await request.body()))
        except ExpatError:
            return Response(status_code=HTTPStatus.BAD_REQUEST.value)

        try:
            for video in self.get_videos_from_body(body):
                if self._video_history.has(video):
                    continue
                await self.on_video(video)
                self._video_history.add(video)
        except (TypeError, KeyError, ValueError):
            return Response(status_code=HTTPStatus.BAD_REQUEST.value)

        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    async def _is_authorized(self, request: Request) -> bool:
        x_hub_signature = request.headers.get("X-Hub-Signature")
        if x_hub_signature is None or "=" not in x_hub_signature:
            return False

        algorithm, value = x_hub_signature.split("=")
        hash_obj = hmac.new(self.password.encode(), await request.body(), algorithm)
        return hmac.compare_digest(hash_obj.hexdigest(), value)
