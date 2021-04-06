import logging
import os

from src.client import Bot

if __name__ == "__main__":
    client = Bot()

    token = os.environ.get("API_KEY", None)
    if token is None:
        logging.error("No token provided ! Quitting")
        exit(1)

    client.run(token)
