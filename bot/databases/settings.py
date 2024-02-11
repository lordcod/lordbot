
from ctypes import util
from email.policy import default
from typing import List, Optional
from discord import RawBulkMessageDeleteEvent
from nextcord import utils
import psycopg2
import re
from psycopg2.extensions import connection


host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
user = 'j5191558_test'
db_name = 'j5191558_test'
password = 'fd5-DVv-pf5-6bx'


def convert_default(default_text: str) -> str:
    if (
        isinstance(default_text, str) and
        (templete := re.fullmatch("'(.+)'::([a-zA-Z0-9]+)", default_text))
    ):
        return templete.group(1)
    return default_text


class Colum:
    def __init__(
        self,
        name: str,
        data_type: str,
        *,
        default: Optional[str] = None,
        primary_key: Optional[bool] = False,
        not_null: Optional[bool] = False,
        _connection: connection
    ) -> None:
        data_type = data_type.upper()

        self.name = name
        self.data_type = data_type
        self.default = default
        self.primary_key = primary_key
        self.not_null = not_null
        self.__connection = _connection

        self.creating_string = (
            f"{name} "
            f"{data_type}"
            f"{' PRIMARY KEY' if primary_key is True else ''}"
            f"{' NOT NULL' if not_null is True else ''}"
            f"{f' DEFAULT {default}' if default is not None else ''}"
        )

    def add_colum(self, table_name: str) -> None:
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    ALTER TABLE {table_name}
                    ADD {self.creating_string};
                """
            )

    def drop_colum(self, table_name: str) -> None:
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    ALTER TABLE {table_name}
                    DROP COLUMN {self.name};
                """
            )

    def change_name(self, table_name: str, new_name: str) -> None:
        self.name = new_name
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    ALTER TABLE {table_name}
                    RENAME COLUMN {self.name} TO {new_name};
                """
            )

    def change_default(self, table_name: str, new_default: str) -> None:
        self.default = new_default
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    ALTER TABLE {table_name}
                    ALTER COLUMN {self.name} SET DEFAULT '{new_default}';
                """
            )

    def change_type(self, table_name: str, new_type: str) -> None:
        self.data_type = new_type
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    ALTER TABLE {table_name}
                    ALTER COLUMN {self.name} TYPE {new_type};
                """
            )

    def __str__(self) -> str:
        return (f"<Colums name=\"{self.name}\" data_type=\"{self.data_type}\" "
                f"default=\"{self.default}\" primary_key={self.primary_key} "
                f"not_null={self.not_null}>")

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
            self.not_null == __value.not_null
        )

    def __ne__(self, __value: object) -> bool:
        if not isinstance(__value, Colum):
            return True
        return (
            self.name != __value.name or
            self.data_type != __value.data_type or
            self.default != __value.default or
            self.primary_key != __value.primary_key or
            self.not_null != __value.not_null
        )


class Table:
    def __init__(
        self,
        *,
        name: str,
        _connection: connection
    ) -> None:
        self.name = name
        self.__connection = _connection

        with _connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {name} ()"
            )

        self.colums = self.get_colums()

        self.reserved_colums = []

    def get_colums(self) -> List[Colum]:
        colums = []
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT c.column_name, c.data_type, c.column_default, is_nullable::bool,
                    CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k 
                        WHERE c.table_name = k.table_name and k.column_name = c.column_name) 
                        THEN true ELSE false END as primary_key
                    FROM INFORMATION_SCHEMA.COLUMNS c 
                    WHERE c.table_name='{self.name}';
                """)
            results = cursor.fetchall()
        for res in results:
            colums.append(Colum(name=res[0],
                                data_type=res[1],
                                default=convert_default(res[2]),
                                not_null=res[3],
                                primary_key=res[4],
                                _connection=self.__connection
                                )
                          )
        return colums

    def add_colum(self, colum: Colum) -> None:
        if not isinstance(colum, Colum):
            raise TypeError('The argument must match the Column type')

        self.reserved_colums.append(colum.name)

        if colum in self.colums:
            return

        if colum_with_name := utils.get(self.colums, name=colum.name):
            if colum.default != colum_with_name.default:
                colum_with_name.change_default(self.name, colum.default)

            if colum.data_type != colum_with_name.data_type:
                colum_with_name.change_type(self.name, colum.data_type)
            return

        colum.add_colum(self.name)
        self.colums.append(colum)

    def delete_by_resed(self):
        for colum in self.colums:
            if colum.name not in self.reserved_colums:
                self.colums.remove(colum)
                colum.drop_colum(self.name)


_connection = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=db_name,
)
_connection.autocommit = True

table = Table(name='roles', _connection=_connection)

guild_id = Colum('guild_id', 'BIGINT', not_null=True, _connection=_connection)
member_id = Colum('member_id', 'BIGINT', not_null=True,
                  _connection=_connection)
roles = Colum('roles', 'JSON', default='{}', _connection=_connection)


print(table.colums)

table.add_colum(guild_id)
table.add_colum(member_id)
table.add_colum(roles)

table.delete_by_resed()

print(table.colums)
