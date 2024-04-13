from .handlers import establish_connection
from .settings import Table, Colum, PostType, set_connection
from .db_engine import DataBase
from .config import (host, port, user, password, db_name)

from bot.resources import info

engine = DataBase.create_engine(host, port, user, password, db_name)

establish_connection(engine)
set_connection(engine)


class GuildsDB(Table):
    __tablename__ = "guilds"

    id = Colum(data_type=PostType.BIGINT, primary_key=True)
    language = Colum(data_type=PostType.TEXT,
                     default=info.DEFAULT_LANGUAGE)
    prefix = Colum(data_type=PostType.TEXT,
                   default=info.DEFAULT_PREFIX)
    color = Colum(data_type=PostType.BIGINT, default=info.DEFAULT_COLOR)
    economic_settings = Colum(data_type=PostType.JSON,
                              default=info.DEFAULT_ECONOMY_SETTINGS)
    music_settings = Colum(data_type=PostType.JSON, default="{}")
    auto_roles = Colum(data_type=PostType.JSON, default="{}")
    invites = Colum(data_type=PostType.JSON, default="{}")
    giveaways = Colum(data_type=PostType.JSON, default="{}")
    tickettool = Colum(data_type=PostType.JSON, default="{}")
    thread_messages = Colum(data_type=PostType.JSON, default="{}")
    reactions = Colum(data_type=PostType.JSON, default="{}")
    auto_translate = Colum(data_type=PostType.JSON, default="{}")
    polls = Colum(data_type=PostType.JSON, default="{}")
    greeting_message = Colum(data_type=PostType.JSON, default="{}")
    command_permissions = Colum(data_type=PostType.JSON, default="{}")
    ideas = Colum(data_type=PostType.JSON, default="{}")


class EconomicDB(Table):
    __tablename__ = "economic"

    guild_id = Colum(data_type=PostType.BIGINT, nullable=True)
    member_id = Colum(data_type=PostType.BIGINT, nullable=True)
    balance = Colum(data_type=PostType.BIGINT, default="0")
    bank = Colum(data_type=PostType.BIGINT, default="0")
    daily = Colum(data_type=PostType.BIGINT, default="0")
    weekly = Colum(data_type=PostType.BIGINT, default="0")
    monthly = Colum(data_type=PostType.BIGINT, default="0")


class RolesDB(Table):
    __tablename__ = "roles"

    guild_id = Colum(data_type=PostType.BIGINT, nullable=True)
    member_id = Colum(data_type=PostType.BIGINT, nullable=True)
    role_id = Colum(data_type=PostType.BIGINT, nullable=True)
    time = Colum(data_type=PostType.BIGINT, nullable=True)


class BansDB(Table):
    __tablename__ = "bans"

    guild_id = Colum(data_type=PostType.BIGINT, nullable=True)
    member_id = Colum(data_type=PostType.BIGINT, nullable=True)
    time = Colum(data_type=PostType.BIGINT, nullable=True)


class MongoDataBases(Table):
    __tablename__ = "mongo"

    name = Colum(data_type=PostType.TEXT, primary_key=True)
    values = Colum(data_type=PostType.JSON, default="{}")


GuildsDB.create_table()
EconomicDB.create_table()
RolesDB.create_table()
BansDB.create_table()
MongoDataBases.create_table()
