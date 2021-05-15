import discord
import os
import re
import random

from src.decorators import log_this_async, require_role
from src.exceptions import CommandNotFoundException, BadFormatException

from src.settings import Settings
from src.game import Game


class CommandManager:
    def __init__(self, client):
        self.client = client
        self.commands = {
            "greet": self.greet,
            "help": self.help,
            "add": self.addWord,
        }
        self.help = Settings.getInstance()["help"]

    @log_this_async
    async def parse_command(self, command):
        """Parse a given string into a dictionnary of information relative to the command

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

        command_dict = {"command": splitted[0][0][1:]}
        command_dict["args"] = [arg[0] if arg[0] != '' else arg[1] for arg in splitted[1:]]

        return {
            "user": command.author,
            "guild": command.guild,
            "channel": command.channel,
            "command": command_dict,
        }

    @require_role("editor")
    @log_this_async
    async def addWord(self, args: dict):
        for word in args["command"]["args"]:
            Game.getInstance().addWord(word, args["user"])

        print("args :", args)

        response = f'**{"**, **".join(args["command"]["args"])}** ajouté{(len(args["command"]["args"]) > 1) * "s"}'
        await args["channel"].send(response)


    @require_role("editor")
    @log_this_async
    async def delWord(self, args: dict):
        pass

    @require_role("player")
    @log_this_async
    async def startGame(self, args: dict):
        pass

    @log_this_async
    async def greet(self, args: dict):
        """Greets the user

        Args:
            args (dict): The argument dictionnary
        """
        greets = ["Hello {}", "Salut {}", "Coucou {}", "Hey {}", "{}, bien ou quoi ?"]
        await args["channel"].send(random.choice(greets).format(args["user"].mention))

    @log_this_async
    async def help(self, args: dict):
        """Displays help messages

        Args:
            args (dict): The argument dictionnary
        """
        if len(args["command"]["args"]) >= 1:
            for command in args["command"]["args"]:
                if command in self.commands.keys():
                    await args["channel"].send(f'```{command} :\n\t{self.help[command]}```')
                else:
                    await args["channel"].send(f"Commande inconnue '{command}'")
        else:
            help_msg = "```"
            for command in self.commands.keys():
                help_msg += f"{command}: \n\t{self.help[command]}\n\n"
            help_msg += "```"
            await args["channel"].send(help_msg)

    @log_this_async
    async def execute(self, command):
        args = await self.parse_command(command)
        if args["command"]["command"] not in self.commands.keys():
            raise CommandNotFoundException(args["command"]["command"])

        else:
            await self.commands[args["command"]["command"]](args)
