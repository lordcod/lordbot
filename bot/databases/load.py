from typing import Any,Dict,Union
import psycopg2
import sys
from bot.misc.logger import Logger


host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
password = 'nVR*6#1P%hyR*4l0'
user = 'j5191558_bot'
db_name = 'j5191558_main'

def load_db():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
    except Exception as err:
        Logger.error(err)
        Logger.error('Failed connection')
        Logger.error('EXIT')
        sys.exit()
    else:
        Logger.success("Successful connection")
        return connection

