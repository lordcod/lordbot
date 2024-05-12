from __future__ import annotations
from typing import Optional, TypeVar, overload
from ..db_engine import DataBase
from ..misc.adapter_dict import Json

T = TypeVar('T')
engine: DataBase = None


class CommandDB:
    def __init__(self, guild_id: int) -> None:
        self.guild_id = guild_id

    @overload
    def get(self, command: str) -> Optional[dict]: ...

    @overload
    def get(self, command: str, default: T) -> dict | T: ...

    def get(self, command: str, default: T = None) -> dict | T:
        data = engine.fetchvalue(
            "SELECT command_permissions ->> %s FROM guilds WHERE id = %s",
            (command, self.guild_id,)
        )

        if not data:
            return default
        return data

    def update(self, key: str, value: dict) -> None:
        value = Json.dumps(value)

        engine.execute(
            """
                UPDATE guilds 
                SET command_permissions = jsonb_set(command_permissions::jsonb, %s, %s) 
                WHERE id = %s
            """,
            ('{'+key+'}', value, self.guild_id, )
        )
