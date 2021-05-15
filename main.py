import logging
import os

from singleton.client import Bot

if __name__ == "__main__":
    client = Bot.getInstance()

    token = os.environ.get("API_KEY", None)
    if token is None:
        logging.error("No token provided ! Quitting")
        exit(1)

    client.run(token)
