import threading
import asyncio

from .load import load_db
from .settings import Table, Colum
from .misc.utils import get_info_colums
from .handlers import (
    establish_connection,
    GuildDateBases,
    EconomyMembedDB,
    CommandDB,
    RoleDateBases,
    MongoDB
)

from bot.resources import info
from bot.misc.logger import Logger

_connection = load_db()


def connection():
    global _connection

    if not _connection.closed == 0:
        Logger.core("[Closed connection] Starting a database reboot")
        _connection = load_db()

    return _connection


class GuildsDB(Table, name="guilds", _connection=_connection):
    id = Colum(data_type="BIGINT", primary_key=True)
    language = Colum(data_type="TEXT",
                     default=info.DEFAULT_LANGUAGE)
    prefix = Colum(data_type="TEXT",
                   default=info.DEFAULT_PREFIX)
    color = Colum(data_type="BIGINT", default=info.DEFAULT_COLOR)
    economic_settings = Colum(data_type="JSON",
                              default=info.DEFAULT_ECONOMY_SETTINGS)
    music_settings = Colum(data_type="JSON", default="{}")
    auto_roles = Colum(data_type="JSON", default="{}")
    thread_messages = Colum(data_type="JSON", default="{}")
    reactions = Colum(data_type="JSON", default="{}")
    auto_translate = Colum(data_type="JSON", default="{}")
    greeting_message = Colum(data_type="JSON", default="{}")
    command_permissions = Colum(data_type="JSON", default="{}")
    ideas = Colum(data_type="JSON", default="{}")


class EconomicDB(Table, name="economic", _connection=_connection):
    guild_id = Colum(data_type="BIGINT", not_null=True)
    member_id = Colum(data_type="BIGINT", not_null=True)
    balance = Colum(data_type="BIGINT", default="0")
    bank = Colum(data_type="BIGINT", default="0")
    daily = Colum(data_type="BIGINT", default="0")
    weekly = Colum(data_type="BIGINT", default="0")
    monthly = Colum(data_type="BIGINT", default="0")


class RolesDB(Table, name="roles", _connection=_connection):
    guild_id = Colum(data_type="BIGINT", not_null=True)
    member_id = Colum(data_type="BIGINT", not_null=True)
    roles = Colum(data_type="JSON", default="{}")


class MongoDataBases(Table, name="mongo", _connection=_connection):
    name = Colum(data_type="TEXT", primary_key=True)
    values = Colum(data_type="JSON", default="{}")


colums = {
    'guilds': get_info_colums('guilds', _connection),
    'economic': get_info_colums('economic', _connection)
}

establish_connection(connection)


def db_forever():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    finally:
        connection().close()
        loop.close()
        exit()


thread = threading.Thread(target=db_forever, name='DataBase')
thread.start()
