from __future__ import annotations
from typing import Callable
from psycopg2.extensions import connection as psycoon
from ..misc.error_handler import on_error
from ..misc.utils import Json

connection: Callable[[], psycoon]

class CommandDB:
    def __init__(self, guild_id: int) -> None:
        self.guild_id = guild_id
    
    @on_error()
    def get(self, command, default) -> dict:
        with connection().cursor() as cursor:
            cursor.execute("SELECT command_permissions ->> %s FROM guilds WHERE id = %s", (command, self.guild_id,))
            
            data = cursor.fetchone()
            if not data[0]:
                return default
            data_new = Json.loads(data[0])
            return data_new
    
    @on_error()
    def update(self,key,value):
        value = Json.dumps(value)
        dkey = (
            '{'
            f'{key}'
            '}'
        )
        
        with connection().cursor() as cursor:
            cursor.execute(
            f"""
                UPDATE 
                    guilds 
                SET 
                    command_permissions = jsonb_set(command_permissions::jsonb, '{dkey}', %s) 
                WHERE 
                    id = %s
            """, 
            (value, self.guild_id, )
            )
    