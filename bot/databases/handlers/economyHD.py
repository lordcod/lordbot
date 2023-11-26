from __future__ import annotations
from typing import Any, Callable
from psycopg2.extensions import connection
from ..misc.error_handler import on_error

class EconomyMembedDB:
    def __init__(self, connection: Callable[[], connection]) -> None:
        self.connection = connection

    def __call__(self, guild_id: int, member_id: int = None) -> EconomyMembedDB:
        self.guild_id = guild_id
        self.member_id = member_id
        return self
    
    @on_error()
    def get(self):
        with self.connection().cursor() as cursor:
            cursor.execute('SELECT * FROM economic WHERE guild_id = %s AND member_id = %s', (self.guild_id,self.member_id))
            
            guild = cursor.fetchone()
            
            return guild
    
    @on_error()
    def insert(self):
        with self.connection().cursor() as cursor:
            cursor.execute('INSERT INTO economic (guild_id,member_id) VALUES (%s,%s)', (self.guild_id,self.member_id))
    
    @on_error()
    def update(self,arg,value):
        if not EconomyMembedDB.get(self.guild_id,self.member_id):
            EconomyMembedDB.insert(self.guild_id,self.member_id)
        
        with self.connection().cursor() as cursor:
            cursor.execute(f'UPDATE economic SET {arg} = %s WHERE guild_id = %s AND member_id = %s', (value, self.guild_id, self.member_id))
            
            self.connection().commit()
    
    @on_error()
    def update_list(self, args):
        for arg in args:
            value = args[arg]
            EconomyMembedDB.update(self.guild_id,self.member_id,arg,value)
    
    @on_error()
    def delete(self):
        with self.connection().cursor() as cursor:
            cursor.execute('DELETE FROM economic WHERE guild_id = %s AND member_id = %s', (self.guild_id,self.member_id))
            
            self.connection().commit()
    
    @on_error()
    def delete_guild(self):
        with self.connection().cursor() as cursor:
            cursor.execute('DELETE FROM economic WHERE guild_id = %s', (self.guild_id,))
            
            self.connection().commit()
