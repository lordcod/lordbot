from bot.misc.logger import Logger
from .config import (host, port, user, password, db_name)
import psycopg2
import sys


def load_db():
    Logger.info("Load DataBases")
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
    except Exception as err:
        Logger.error(err)
        Logger.error('Failed connection')
        Logger.critical('Starting a database reboot')
        
        sys.exit()
    else:
        Logger.success("Successful connection")
        return connection

