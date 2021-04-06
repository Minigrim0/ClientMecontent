import discord
from src.commands_manager import CommandsManager


class Bot(discord.Client):
    def __init__(self):
        self.command_manager = CommandsManager(client)

    async def on_ready(self):
        logging.info('Logged in as {0.user}'.format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('!'):
            self.command_manager.execute(command=message)
