import logging

import discord

from singleton.settings import Settings


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

        from src.command_manager import CommandManager

        self.command_manager = CommandManager(self)

        super().__init__()

    async def on_ready(self):
        logging.debug(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!"):
            await self.command_manager.execute(command=message)

    def getChannel(self, channel_name: str) -> discord.channel:
        """Returns the channel corresponding to the given name

        Args:
            channel_name (str): the name of the channel (in the settings file)

        Returns:
            discord.channel: The corresponding discord channel
        """
        channel_id = Settings.getInstance()["channels"][channel_name]
        return self.get_channel(int(channel_id))
