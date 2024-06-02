from bot.misc import logger
from bot import main
import logging
import nextcord


if __name__ == "__main__":
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith('nextcord'):
            _log_nextcord = logging.getLogger(logger_name)
            _log_nextcord.setLevel(logging.INFO)
    main.start_bot()
