import threading
import asyncio

from .load import load_db
from .misc.error_handler import on_error
from .misc.utils import get_info_colums, register_table
from .handlers import GuildDateBasesInstance, EconomyMembedDBInstance, CommandDBInstance, RolesDBInstance

from bot.misc.logger import Logger

_connection = load_db()

def connection():
    global _connection
    
    if not _connection.closed == 0 :
        Logger.core("[Closed connection] Starting a database reboot")
        _connection = load_db()
    
    return _connection

register_table(
    table_name="guilds",
    variable=(
        "id INT8 PRIMARY KEY,"
        "language TEXT DEFAULT 'en',"
        "prefix TEXT DEFAULT 'l.',"
        "color INT8 DEFAULT '1974050',"
        "economic_settings JSON DEFAULT '{\"emoji\":\"<:diamond:1183363436780978186>\"}',"
        "auto_roles JSON DEFAULT '{}',"
        "thread_messages JSON DEFAULT '{}',"
        "reactions JSON DEFAULT '{}',"
        "auto_translate JSON DEFAULT '{}',"
        "greeting_message JSON DEFAULT '{}',"
        "disabled_commands JSON DEFAULT '{}'"
    ),
    connection=_connection
)

register_table(
    table_name="economic",
    variable=(
        "guild_id INT8 NOT NULL,"
        "member_id INT8 NOT NULL,"
        "balance INT8 DEFAULT '0',"
        "bank INT8 DEFAULT '0',"
        "daily INT8 DEFAULT '0',"
        "weekly INT8 DEFAULT '0',"
        "monthly INT8 DEFAULT '0'"
    ),
    connection=_connection
)

register_table(
    table_name="roles",
    variable=(
        "guild_id INT8 NOT NULL,"
        "member_id INT8 NOT NULL,"
        "roles JSON DEFAULT '{}'"
    ),
    connection=_connection
)

colums = {
    'guilds':get_info_colums('guilds', _connection),
    'economic':get_info_colums('economic', _connection)
}


GuildDateBases = GuildDateBasesInstance(connection)
EconomyMembedDB = EconomyMembedDBInstance(connection)
CommandDB = CommandDBInstance(connection)
RolesDB = RolesDBInstance(connection)

def db_forever():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        connection().close()
        loop.close()
        exit()

thread = threading.Thread(target=db_forever,name='DataBase')
thread.start()