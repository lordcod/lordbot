import logging
from bot import main

logging.basicConfig(
    filename="bot.log",
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s"
)


if __name__ == "__main__":
    main.start_bot()
