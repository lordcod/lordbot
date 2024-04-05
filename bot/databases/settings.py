from __future__ import annotations
from typing import List, Optional
from nextcord import utils
import re
import enum
from .db_engine import DataBase

engine: DataBase = None


def convert_default(default_text: str) -> str:
    if (
        isinstance(default_text, str) and
        (templete := re.fullmatch("'(.+)'::([a-zA-Z0-9]+)", default_text))
    ):
        return templete.group(1)
    return default_text


def set_connection(db: DataBase) -> None:
    global engine
    engine = db


class PostType(enum.StrEnum):
    BIGINT = "BIGINT"
    BIGSERIAL = "BIGSERIAL"
    BIT = "BIT"
    BIT_VATYING = "BIT VATYING"
    BOOLEAN = "BOOLEAN"
    BOX = "BOX"
    BYTEA = "BYTEA"
    BYNARY = "BYNARY"
    CHARACTER = "CHARACTER"
    CHARACTER_VARYING = "CHARACTER VARYING"
    CIDR = "CIDR"
    CIRCLE = "CIRCLE"
    DATE = "DATE"
    DOUBLE_PRECISION = "DOUBLE PRECISION"
    INET = "INET"
    INTEGER = "INTEGER"
    INTERVAL = "INTERVAL"
    JSON = "JSON"
    JSONB = "JSONB"
    LINE = "LINE"
    LSEG = "LSEG"
    MACADDR = "MACADDR"
    MACADDR8 = "MACADDR8"
    MONEY = "MONEY"
    NUMERIC = "NUMERIC"
    PATH = "PATH"
    PG_LSN = "PG_LSN"
    PG_SNAPSHOT = "PG_SNAPSHOT"
    POINT = "POINT"
    POLYGON = "POLYGON"
    REAL = "REAL"
    SMALLINT = "SMALLINT"
    SMALLSERIAL = "SMALLSERIAL"
    SERIAL = "SERIAL"
    TEXT = "TEXT"
    TIME = "TIME"
    TIMESTAMP = "TIMESTAMP"
    TSQUERY = "TSQUERY"
    TSVECTOR = "TSVECTOR"
    TXID_SNAPSHOT = "TXID_SNAPSHOT"
    UUID = "UUID"
    XML = "XML"

    @classmethod
    def get(cls, value: str) -> PostType:
        return cls(value.upper())


class Colum:
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        data_type: str,
        default: Optional[str] = None,
        primary_key: Optional[bool] = False,
        nullable: Optional[bool] = False
    ) -> None:

        data_type = data_type.upper()

        self.name = name
        self.data_type = data_type if isinstance(
            data_type, PostType) else PostType.get(data_type)
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def add_colum(self, table_name: str) -> None:
        engine.execute(
                f"""
                    ALTER TABLE {table_name}
                    ADD {self.name} {self.data_type.value}
                    {" PRIMARY KEY" if self.primary_key is True else ""}
                    {" NOT NULL" if self.nullable is True else ""}
                    {f" DEFAULT '{self.default}'" if self.default is not None else ""}
                """
        )

    def drop_colum(self, table_name: str) -> None:
        engine.execute(
                f"""
                    ALTER TABLE {table_name}
                    DROP COLUMN {self.name};
                """
        )

    def change_name(self, table_name: str, new_name: str) -> None:
        self.name = new_name
        engine.execute(
                f"""
                    ALTER TABLE {table_name}
                    RENAME COLUMN {self.name} TO {new_name};
                """
        )

    def change_default(self, table_name: str, new_default: str) -> None:
        self.default = new_default
        engine.execute(
                f"""
                    ALTER TABLE {table_name}
                    ALTER COLUMN {self.name} SET DEFAULT '{new_default}';
                """
        )

    def change_type(self, table_name: str, new_type: PostType) -> None:
        engine.execute(
                f"""
                    ALTER TABLE {table_name}
                    ALTER COLUMN {self.name} TYPE {new_type.value};
                """
        )

    def __str__(self) -> str:
        return (f"<Colums name=\"{self.name}\" data_type=\"{self.data_type}\" "
                f"default=\"{self.default}\" primary_key={self.primary_key} "
                f"nullable={self.nullable}>")

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Colum):
            return False
        return (
            self.name == __value.name and
            self.data_type == __value.data_type and
            self.default == __value.default and
            self.primary_key == __value.primary_key and
            self.nullable == __value.nullable
        )

    def __ne__(self, __value: object) -> bool:
        if not isinstance(__value, Colum):
            return True
        return (
            self.name != __value.name or
            self.data_type != __value.data_type or
            self.default != __value.default or
            self.primary_key != __value.primary_key or
            self.nullable != __value.nullable
        )


class TableAPI:
    @staticmethod
    def get_colums(table_name: str) -> List[Colum]:
        colums = []
        results = engine.fetchall("""
                    SELECT c.column_name, c.data_type, c.column_default, is_nullable::bool,
                    CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k 
                        WHERE c.table_name = k.table_name and k.column_name = c.column_name) 
                        THEN true ELSE false END as primary_key
                    FROM INFORMATION_SCHEMA.COLUMNS c 
                    WHERE c.table_name=%s;
                """, (table_name,))
        for res in results:
            colums.append(Colum(
                name=res[0],
                data_type=res[1],
                default=convert_default(res[2]),
                nullable=res[3],
                primary_key=res[4]
            ))
        return colums

    @staticmethod
    def add_colum(table_name, colum: Colum, colums: List[Colum]) -> None:
        if not isinstance(colum, Colum):
            raise TypeError("The argument must match the Column type")

        if colum in colums:
            return

        if colum_with_name := utils.get(colums, name=colum.name):
            if colum.default != colum_with_name.default:
                colum_with_name.change_default(table_name, colum.default)

            if colum.data_type != colum_with_name.data_type:
                colum_with_name.change_type(table_name, colum.data_type)
            return

        colum.add_colum(table_name)
        colums.append(colum)

    @staticmethod
    def delete_ofter_colums(
        table_name: str,
        colums: List[Colum],
        reserved_colums: List[str]
    ) -> None:
        for colum in colums:
            if colum.name not in reserved_colums:
                colums.remove(colum)
                colum.drop_colum(table_name)


class Table:
    def __init_subclass__(
        cls,
        *,
        force_colums: bool = True
    ) -> None:
        cls.__tablename__ = (cls.__tablename__ or cls.__name__).lower()
        cls.force_colums = force_colums

    @classmethod
    def create_table(cls):
        engine.execute(
            f"CREATE TABLE IF NOT EXISTS {cls.__tablename__} ()")

        cls.colums = TableAPI.get_colums(cls.__tablename__)
        reserved_colums = []

        for name, item in cls.__dict__.items():
            if not isinstance(item, Colum):
                continue
            item.name = item.name or name
            reserved_colums.append(item.name)
            TableAPI.add_colum(cls.__tablename__, item, cls.colums)
        if cls.force_colums is True:
            TableAPI.delete_ofter_colums(
                cls.__tablename__, cls.colums, reserved_colums)
