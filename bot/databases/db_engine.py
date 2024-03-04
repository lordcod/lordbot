from __future__ import annotations
from typing import Any, Mapping, Sequence
import psycopg2
from bot.misc.logger import Logger


Vars = Sequence[Any] | Mapping[str, Any] | None
i = 0


class DataBase:
    conn_kwargs: dict

    def __init__(
        self,
        __connection: psycopg2.extensions.connection
    ) -> None:
        self.__connection = __connection

    @property
    def connection(self) -> psycopg2.extensions.connection:
        if self.__connection.closed != 0:
            Logger.core("[Closed connection] Starting a database reboot")
            self.__connection = psycopg2.connect(**self.conn_kwargs)
            self.__connection.autocommit = True
        return self.__connection

    @classmethod
    def create_engine(
        cls,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str
    ) -> DataBase:
        Logger.info("Load DataBases")
        try:
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            connection.autocommit = True
        except Exception as err:
            Logger.error(err)
            Logger.error('Failed connection')
            Logger.critical(
                'The database could not be loaded and the program is terminated because of this')

            raise err
        else:
            Logger.success("Successful connection")
            self = cls(connection)
            self.conn_kwargs = {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "database": database
            }
            return self

    def execute(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(query, vars)

    def fetchall(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> list[tuple[Any, ...]]:
        with self.connection.cursor() as cursor:
            cursor.execute(query, vars)
            return cursor.fetchall()

    def fetchmany(
        self,
        query: str | bytes,
        vars: Vars = None,
        size: int | None = None
    ) -> list[tuple[Any, ...]]:
        with self.connection.cursor() as cursor:
            cursor.execute(query, vars)
            return cursor.fetchmany(size)

    def fetchone(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> tuple[Any, ...] | None:
        with self.connection.cursor() as cursor:
            cursor.execute(query, vars)
            return cursor.fetchone()
