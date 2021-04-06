import discord
import os
import re
import asyncio

from src.decorators import log_this_async, require_role
from src.exceptions import CommandNotFoundException, BadFormatException


class CommandManager:
    def __init__(self, client):
        self.client = client
        self.commands = {"greet": self.greet}

    @log_this_async
    async def parse_command(self, command):
        """Parse a given string into a dictionnary of information relative to the command
            Example :
                !addword Test
                returns :
                    {
                        "user": "User",
                        "guild": "Guild",
                        "channel": "Channel",
                        "command": {
                            "command": "$Command",
                            "args": "$Args"
                        }
                    }

        Args:
            command (string): The command the user typed

        Returns:
            Infos: An dictionnary containing the information
        """

        regex = r"^!([a-zA-Z0-9])+( (([a-zA-Z0-9?!'éèàù\-_])+|(\"([a-zA-Z0-9?!'éèàù\-_ ])+\")))*?$"
        if not re.match(regex, command.content):
            raise BadFormatException(command=command.content, pattern=regex)

        splitted = re.findall(
            r"((?:[a-zA-Z0-9?!'éèàù\-_])+)|\"((?:[a-zA-Z0-9?!'éèàù\-_ ])+)\"",
            command.content,
        )

        command_dict = {"command": splitted[0][0][1:], "args": splitted[1:]}

        return {
            "user": command.author,
            "guild": command.guild,
            "channel": command.channel,
            "command": command_dict,
        }

    @require_role("Photographe Professionel", "Maitre des mots")
    @log_this_async
    async def addWord(self, args: dict):
        pass

    @require_role("Photographe Professionel", "Maitre des mots")
    @log_this_async
    async def delWord(self, args: dict):
        pass

    @require_role("Photographe Professionel", "Photographe")
    @log_this_async
    async def startGame(self, args: dict):
        pass

    @log_this_async
    def greet(self, args: dict):
        pass

    @log_this_async
    async def execute(self, command):
        parsed = await self.parse_command(command)
        if parsed["command"]["command"] not in self.commands.keys():
            raise CommandNotFoundException(parsed["command"]["command"])
