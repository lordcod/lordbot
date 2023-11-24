import psycopg2
from bot.misc.logger import Logger
import time
from .config import (host, user, password, db_name)



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
        Logger.critical('Starting a database reboot')
        
        time.sleep(15)
        
        return load_db()
    else:
        Logger.success("Successful connection")
        return connection

