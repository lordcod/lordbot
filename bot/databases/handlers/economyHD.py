from __future__ import annotations
from typing import Callable
from psycopg2.extensions import connection as psycoon
from ..misc.error_handler import on_error

connection: Callable[[], psycoon]

class EconomyMembedDB:
    def __init__(self, guild_id: int, member_id: int = None) -> None:
        self.guild_id = guild_id
        self.member_id = member_id
    
    
    @on_error()
    def get_leaderboards(self):
        with connection().cursor() as cursor:
            cursor.execute(
                """SELECT 
                member_id, balance, bank, balance+bank as total
                FROM economic
                WHERE guild_id = %s
                ORDER BY total DESC;""", 
                (self.guild_id,)
            )
            
            guild = cursor.fetchall()
            
            return guild
    
    @on_error()
    def get(self):
        with connection().cursor() as cursor:
            cursor.execute('SELECT * FROM economic WHERE guild_id = %s AND member_id = %s', (self.guild_id,self.member_id))
            
            guild = cursor.fetchone()
            
            return guild
    
    @on_error()
    def insert(self):
        with connection().cursor() as cursor:
            cursor.execute('INSERT INTO economic (guild_id,member_id) VALUES (%s,%s)', (self.guild_id,self.member_id))
    
    @on_error()
    def update(self,arg,value):
        if not self.get():
            self.insert()
        
        with connection().cursor() as cursor:
            cursor.execute(f'UPDATE economic SET {arg} = %s WHERE guild_id = %s AND member_id = %s', (value, self.guild_id, self.member_id))
    
    @on_error()
    def update_list(self, args):
        for key in args:
            value = args[key]
            self.update(key,value)
    
    @on_error()
    def delete(self):
        with connection().cursor() as cursor:
            cursor.execute('DELETE FROM economic WHERE guild_id = %s AND member_id = %s', (self.guild_id,self.member_id))
    
    @on_error()
    def delete_guild(self):
        with connection().cursor() as cursor:
            cursor.execute('DELETE FROM economic WHERE guild_id = %s', (self.guild_id,))
