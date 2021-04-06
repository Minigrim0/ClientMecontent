import discord
import os
import re
import asyncio

from src.decorators import log_this, require_role


class CommandsManager:
    def __init__(self, client):
        self.client = client
        self.commands = {
            "greet": self.greet
        }

    def parse_command(self, command):
        """Parse a given string into a dictionnary of information relative to the command
            Example :
                !addword Test
                returns : 
                    {
                        "user": "$UserID",
                        "guild": "$GuildID",
                        "channel": "$ChannelID",
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
        infos = {
            "user": command.author.id,
            "guild": message.guild,
            "channel": message.channel,
        }
        
        return infos

    @require_role("Photographe Professionel", "Maitre des mots")
    @log_this
    async def addWord(self, args: dict):
        pass

    @require_role("Photographe Professionel", "Maitre des mots")
    @log_this
    async def delWord(self, args: dict):
        pass

    @require_role("Photographe Professionel", "Photographe")
    @log_this
    async def startGame(self, args: dict):
        pass

    @log_this
    def greet(self, args: dict):
        pass

    @log_this
    def execute(self, command):
        parsed = self.parse_command(command)
        if parsed["command"]["command"] not in self.commands.keys():
            raise CommandNotFound(parsed["command"]["command"])
