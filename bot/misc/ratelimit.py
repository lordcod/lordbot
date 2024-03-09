import time
import nextcord

import enum
from typing import Union


data = {}


class BucketType(enum.IntEnum):
    MEMBER = 0
    SERVER = 1


class CooldownGuild:
    def __init__(
        self,
        command_name: str,
        command_data: dict,
        guild_id: int
    ) -> None:
        self.command_name = command_name
        self.command_data = command_data
        self.guild_id = guild_id

        self.check_register()

    def check_register(self) -> None:
        data.setdefault(self.guild_id, {})
        data[self.guild_id].setdefault(self.command_name, {})

    def get(self) -> Union[None, float]:
        cooldata: dict = data[self.guild_id][self.command_name]

        regular_rate: int = self.command_data.get('rate')
        rate: int = cooldata.get('rate', 0)
        per: float = cooldata.get('per', 0)

        if time.time() >= per:
            self.reset()
            return None

        if regular_rate > rate:
            return None

        return round(per-time.time(), 2)

    def add(self) -> None:
        global data

        cooldata: dict = data[self.guild_id][self.command_name]
        rate: int = cooldata.get('rate', 0)
        per: float = cooldata.get('per', 0)

        regular_per: int = self.command_data.get('per')

        datatime = time.time()+regular_per if rate == 0 else per

        data[self.guild_id][self.command_name] = {
            'rate': rate+1,
            'per': datatime
        }

    def take(self) -> None:
        global data

        cooldata: dict = data[self.guild_id][self.command_name]
        rate: int = cooldata.get('rate', 0)
        per: float = cooldata.get('per', 0)

        datarate = 0 if 0 >= (rate-1) else rate-1

        data[self.guild_id][self.command_name] = {
            'rate': datarate,
            'per': per
        }

    def reset(self) -> None:
        data[self.guild_id][self.command_name] = {
            'rate': 0,
            'per': 0
        }


class CooldownMember:
    def __init__(
        self,
        command_name: str,
        command_data: dict,
        guild_id: int,
        member_id: int
    ) -> None:
        self.command_name = command_name
        self.command_data = command_data
        self.guild_id = guild_id
        self.member_id = member_id

        self.check_register()

    def check_register(self) -> None:
        data.setdefault(self.guild_id, {})
        data[self.guild_id].setdefault(self.command_name, {})
        data[self.guild_id][self.command_name].setdefault(self.member_id, {})

    def get(self) -> Union[None, float]:
        cooldata: dict = data[self.guild_id][self.command_name][self.member_id]

        regular_rate: int = self.command_data.get('rate')
        rate: int = cooldata.get('rate', 0)
        per: float = cooldata.get('per', 0)

        if time.time() >= per:
            self.reset()
            return None

        if regular_rate > rate:
            return None

        return round(per-time.time(), 2)

    def add(self) -> None:
        global data

        cooldata: dict = data[self.guild_id][self.command_name][self.member_id]
        rate: int = cooldata.get('rate', 0)
        per: float = cooldata.get('per', 0)

        regular_per: int = self.command_data.get('per')

        newper = time.time()+regular_per if rate == 0 else per

        data[self.guild_id][self.command_name][self.member_id] = {
            'rate': rate+1,
            'per': newper
        }

    def take(self) -> None:
        global data

        cooldata: dict = data[self.guild_id][self.command_name][self.member_id]
        rate: int = cooldata.get('rate', 0)
        per: float = cooldata.get('per', 0)

        newrate = max(rate-1, 0)

        data[self.guild_id][self.command_name][self.member_id] = {
            'rate': newrate,
            'per': per
        }

    def reset(self) -> None:
        data[self.guild_id][self.command_name][self.member_id] = {
            'rate': 0,
            'per': 0
        }


CooldownObject = Union[CooldownGuild, CooldownMember]


class Cooldown:
    @classmethod
    def from_message(
        cls,
        command_name: str,
        command_data: dict,
        message: nextcord.Message
    ) -> CooldownObject:
        cooldata: dict = command_data
        cooltype = cooldata.get('type')

        if cooltype == BucketType.MEMBER:
            return CooldownMember(
                command_name,
                command_data,
                message.guild.id,
                message.author.id
            )
        elif cooltype == BucketType.SERVER:
            return CooldownGuild(
                command_name,
                command_data,
                message.guild.id
            )
        else:
            raise ValueError()


def reset_cooldown(guild_id: int, command_name: str) -> None:
    data.get(guild_id, {}).pop(command_name)
