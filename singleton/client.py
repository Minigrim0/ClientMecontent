import logging

import discord
from src.command_manager import CommandManager


class Bot(discord.Client):
    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            Bot: The instance
        """
        if Bot.instance is None:
            Bot()
        return Bot.instance

    def __init__(self):
        if self.instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Bot.instance = self

        self.command_manager = CommandManager(self)

        super().__init__()

    async def on_ready(self):
        logging.debug(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!"):
            await self.command_manager.execute(command=message)
