from __future__ import annotations
from ..db_engine import DataBase
from ..misc.error_handler import on_error
from ..misc.utils import Json

engine: DataBase = None


class CommandDB:
    def __init__(self, guild_id: int) -> None:
        self.guild_id = guild_id

    @on_error()
    def get(self, command, default=None) -> dict:
        data = engine.fetchone(
            "SELECT command_permissions ->> %s FROM guilds WHERE id = %s",
            (command, self.guild_id,)
        )

        if not data[0]:
            return default
        data_new = Json.loads(data[0])
        return data_new

    @on_error()
    def update(self, key, value):
        value = Json.dumps(value)

        engine.execute(
            """
                UPDATE guilds 
                SET command_permissions = jsonb_set(command_permissions::jsonb, %s, %s) 
                WHERE id = %s
            """,
            ('{'+key+'}', value, self.guild_id, )
        )
