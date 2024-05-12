import nextcord


import random
from typing import Union, Optional, Dict

ffmpeg_path = "ffmpeg"
initally_num = 10


def addtional_convert(timestamp: int):
    if 10 > timestamp:
        return f"0{timestamp}"
    return str(timestamp)


def convertor_time(timestamp: Union[int, float]):
    timestamp = int(timestamp)

    seconds = addtional_convert(timestamp % 60)
    minutes = addtional_convert(timestamp // 60)

    return f"{minutes}:{seconds}"


class Queue:
    def __init__(self) -> None:
        self.data = {}

    def token_generate(self) -> int:
        val = random.randint(1000000, 9999999)
        return val

    def register_guild(self, guild_id):
        self.data.setdefault(guild_id, [])

    def get_all(self, guild_id):
        self.register_guild(guild_id)

        return self.data[guild_id]

    def add(self, guild_id, track) -> int:
        self.register_guild(guild_id)

        self.data[guild_id].append(track)

        return track.id

    def remove(self, guild_id, token: Optional[int] = None) -> None:
        self.register_guild(guild_id)
        data = self.get(guild_id)

        if data is not None and (token is None or data.id == token):
            self.data[guild_id].pop(0)

    def clear(self, guild_id) -> None:
        self.data[guild_id] = []

    def get(self, guild_id):
        self.register_guild(guild_id)
        try:
            return self.data[guild_id][0]
        except IndexError:
            return None

    def index(self, guild_id, index) -> Optional[Track]:
        self.register_guild(guild_id)
        try:
            return self.data[guild_id][index]
        except IndexError:
            return None

    def set(self, guild_id, tracks) -> None:
        self.register_guild(guild_id)
        self.data[guild_id] = tracks


class MusicPlayer:
    def __init__(self,
                 voice: Union[nextcord.VoiceClient, nextcord.VoiceProtocol],
                 message: nextcord.Message,
                 guild_id: int) -> None:
        self.voice = voice
        self.message = message
        self.guild_id = guild_id

    async def process(self, token: Optional[int] = None):
        self.data = queue.get(self.guild_id)

        if self.data is None:
            await self.message.edit(
                content="I didn't find any tracks in the queue, "
                        "so I finished the job!",
                embed=None,
                view=None
            )
            await self.voice.disconnect()
            return
        elif self.guild_id in current_players:
            await self.message.edit(
                content="The track has been added to the queue!",
                embed=None,
                view=None
            )
            return
        current_players[self.guild_id] = self

        await self.play()

    async def update_message(self):
        embed = nextcord.Embed(
            title=f"{self.data.title} - {', '.join(self.data.artist_names)}",
            description=convertor_time(self.data.diration),
            url=self.data.get_url()
        )
        embed.set_thumbnail(self.data.get_image())

        await self.message.edit(
            content=None,
            embed=embed,
            view=None
        )

    async def callback(self, err):
        queue.remove(self.guild_id, self.data.id)
        current_players.pop(self.guild_id)

        player = self.__class__(self.voice, self.message, self.guild_id)
        await player.process()

    async def move_to(self, index: int) -> None:
        track = queue.index(self.guild_id, index)
        if track is None:
            raise IndexError("Track at index %s was not found." % index)
        tracks = queue.data[self.guild_id][index:]
        tracks.insert(0, self.data)
        queue.set(self.guild_id, tracks)
        self.voice.stop()

    async def skip(self):
        self.voice.stop()

    async def stop(self):
        self.voice.stop()
        queue.clear(self.guild_id)
        current_players.pop(self.guild_id)

    async def play(self):
        await self.update_message()

        music_url = await self.data.download_link()
        source = nextcord.FFmpegPCMAudio(
            music_url, executable=ffmpeg_path, pipe=False)
        source = nextcord.PCMVolumeTransformer(source, volume=0.5)

        self.voice.play(source, after=self.callback)


current_players: Dict[int, MusicPlayer] = {}
queue = Queue()
