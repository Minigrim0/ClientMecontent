import logging
import os

import discord

from src.client import bot


client = Bot()

token = os.environ.get('API_KEY', None)
if token is None:
    logging.error("No token provided ! Quitting")
    exit(1)

client.run(token)
