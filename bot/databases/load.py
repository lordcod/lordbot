import psycopg2
from bot.misc.logger import Logger
import time


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
        time.sleep(5)
        Logger.critical('Starting a database reboot')
        load_db()
    else:
        Logger.success("Successful connection")
        return connection

