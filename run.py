import logging
from bot import main

_log = logging.basicConfig(
    filename="bot.log",
    level=logging.DEBUG
)

if __name__ == "__main__":
    main.start_bot()
