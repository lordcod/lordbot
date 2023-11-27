from bot.misc.logger import Logger
from .config import (host, port, user, password, db_name)
import psycopg2
import time
import sys


def load_db(attempt=0):
    if attempt > 3:
        sys.exit()
    
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
        
        time.sleep(300)
        
        load_db(attempt+1)
    else:
        Logger.success("Successful connection")
        return connection

