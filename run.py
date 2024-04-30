import logging
from bot import main


_log = logging.basicConfig(
    filename="botlog.txt",
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s"
)


if __name__ == "__main__":
    main.start_bot()
