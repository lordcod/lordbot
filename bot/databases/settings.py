from typing import List, Optional
from nextcord import utils
import re
from psycopg2.extensions import connection


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
        *,
        name: Optional[str] = None,
        data_type: str,
        default: Optional[str] = None,
        primary_key: Optional[bool] = False,
        not_null: Optional[bool] = False,
        _connection: Optional[connection] = None
    ) -> None:

        data_type = data_type.upper()

        self.name = name
        self.data_type = data_type
        self.default = default
        self.primary_key = primary_key
        self.not_null = not_null
        self.__connection = _connection

    def update_connection(self, _connection: connection) -> None:
        self.__connection = self.__connection or _connection

    def add_colum(self, table_name: str) -> None:
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    ALTER TABLE {table_name}
                    ADD {self.name} {self.data_type}
                    {" PRIMARY KEY" if self.primary_key is True else ""}
                    {" NOT NULL" if self.not_null is True else ""}
                    {f" DEFAULT '{self.default}'" if self.default is not None else ""}
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
    def __init_subclass__(cls,
                          *,
                          name: Optional[str] = None,
                          force_colums: Optional[bool] = True,
                          _connection: connection) -> None:
        cls.name = (name or cls.__name__).lower()
        cls.__connection = _connection

        with _connection.cursor() as cursor:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {cls.name} ()")

        cls.colums = cls.get_colums()
        cls.reserved_colums = []

        for name, item in cls.__dict__.items():
            if not isinstance(item, Colum):
                continue
            item.name = item.name or name
            item.update_connection(_connection)
            cls.add_colum(item)
        if force_colums is True:
            cls.delete_by_resed()

    @classmethod
    def get_colums(cls) -> List[Colum]:
        colums = []
        with cls.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT c.column_name, c.data_type, c.column_default, is_nullable::bool,
                    CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k 
                        WHERE c.table_name = k.table_name and k.column_name = c.column_name) 
                        THEN true ELSE false END as primary_key
                    FROM INFORMATION_SCHEMA.COLUMNS c 
                    WHERE c.table_name='{cls.name}';
                """)
            results = cursor.fetchall()
        for res in results:
            colums.append(Colum(name=res[0],
                                data_type=res[1],
                                default=convert_default(res[2]),
                                not_null=res[3],
                                primary_key=res[4],
                                _connection=cls.__connection
                                ))
        return colums

    @classmethod
    def add_colum(cls, colum: Colum) -> None:
        if not isinstance(colum, Colum):
            raise TypeError("The argument must match the Column type")

        cls.reserved_colums.append(colum.name)

        if colum in cls.colums:
            return

        if colum_with_name := utils.get(cls.colums, name=colum.name):
            if colum.default != colum_with_name.default:
                colum_with_name.change_default(cls.name, colum.default)

            if colum.data_type != colum_with_name.data_type:
                colum_with_name.change_type(cls.name, colum.data_type)
            return

        colum.add_colum(cls.name)
        cls.colums.append(colum)

    @classmethod
    def delete_by_resed(cls):
        for colum in cls.colums:
            if colum.name not in cls.reserved_colums:
                cls.colums.remove(colum)
                colum.drop_colum(cls.name)

    @classmethod
    def delete(cls):
        with cls.__connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT c.column_name, c.data_type, c.column_default, is_nullable::bool,
                    CASE WHEN EXISTS(SELECT 1 FROM INFORMATION_SCHEMA.constraint_column_usage k 
                        WHERE c.table_name = k.table_name and k.column_name = c.column_name) 
                        THEN true ELSE false END as primary_key
                    FROM INFORMATION_SCHEMA.COLUMNS c 
                    WHERE c.table_name='{cls.name}';
                """)
