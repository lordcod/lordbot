from __future__ import annotations
from typing import Optional, TypeVar, overload
from ..db_engine import DataBase

T = TypeVar('T')
engine: DataBase = None


class CommandDB:
    def __init__(self, guild_id: int) -> None:
        self.guild_id = guild_id

    @overload
    async def get(self, command: str) -> Optional[dict]: ...

    @overload
    async def get(self, command: str, default: T) -> T: ...

    async def get(self, command: str, default: T = None) -> dict | T:
        data = await engine.fetchvalue(
            "SELECT command_permissions ->> $1 FROM guilds WHERE id = $2",
            (command, self.guild_id,)
        )

        if not data:
            return default
        return data

    async def update(self, key: str, value: dict) -> None:
        await engine.execute(
            """
                UPDATE guilds 
                SET command_permissions = jsonb_set(command_permissions::jsonb, $1, $2) 
                WHERE id = $3
            """,
            ('{'+key+'}', value, self.guild_id, )
        )
