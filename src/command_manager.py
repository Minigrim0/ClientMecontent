import re
import random

from discord import Embed
from discord.utils import get

from src.decorators import log_this_async, require_role, require_parameters
from src.exceptions import CommandNotFoundException, BadFormatException

from singleton.settings import Settings
from singleton.game import Game
from singleton.user import User
from singleton.word import Word


class CommandManager:
    def __init__(self, client):
        self.client = client
        self.commands = {
            "greet": self.greet,
            "help": self.help,
            "wadd": self.addWord,
            "wdel": self.delWord,
            "wlist": self.listWord,
            "register": self.register,
            "score": self.getScore,
            "new": self.newGame,
            "start": self.startGame,
            "join": self.joinGame,
            "leave": self.leaveGame,
            "info": self.gameInfo,
        }
        self.help = Settings.getInstance()["help"]

    async def parse_command(self, command):
        """Parse a given string into a dictionnary of information relative to the command

        Args:
            command (string): The command the user typed

        Returns:
            Infos: An dictionnary containing the information
        """

        regex = r"^!([a-zA-Z0-9])+( (([<@&#>a-zA-Z0-9?!',éèàù\-_])+|(\"([<@&#>a-zA-Z0-9?!',éèàù\-_ ])+\")))*?$"
        if not re.match(regex, command.content):
            raise BadFormatException(command=command.content, pattern=regex)

        splitted = re.findall(
            r"((?:[<@&#>a-zA-Z0-9?!'éèàù\-_])+)|\"((?:[<@&#>a-zA-Z0-9?!',éèàù\-_ ])+)\"",
            command.content,
        )

        command_dict = {"command": splitted[0][0][1:]}
        command_dict["args"] = [arg[0] if arg[0] != "" else arg[1] for arg in splitted[1:]]

        return {
            "user": command.author,
            "guild": command.guild,
            "channel": command.channel,
            "command": command_dict,
        }

    @require_role("player")
    @log_this_async
    async def newGame(self, args: dict):
        game_id = Game.getInstance().createGame(args["command"]["args"], args["user"].id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=str(game_id)))

    @require_parameters(1)
    @log_this_async
    async def gameInfo(self, args: dict):
        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=args["command"]["args"][0]))

    @require_parameters(1)
    @log_this_async
    async def joinGame(self, args: dict):
        game_id = args["command"]["args"][0]
        Game.getInstance().addUserToGame(args["user"].id, game_id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=game_id))

    @require_parameters(1)
    @log_this_async
    async def leaveGame(self, args: dict):
        game_id = args["command"]["args"][0]
        Game.getInstance().removeUserFromGame(args["user"].id, game_id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=game_id))

    @require_role("player")
    @require_parameters(1)
    @log_this_async
    async def startGame(self, args: dict):
        game_id = args["command"]["args"][0]
        Game.getInstance().startGame(game_id=game_id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=game_id))

    @log_this_async
    async def register(self, args: dict):
        if not User.getInstance().exists(args["user"]):
            User.getInstance().addUser(args["user"])
            role = get(args["guild"].roles, id=int(Settings.getInstance()["roles"]["player"]))
            await args["user"].add_roles(role)
            await args["channel"].send("Tu es maintenant un photographe !")
        else:
            await args["channel"].send("Tu es déjà enregistré !")

    @require_role("player")
    @log_this_async
    async def getScore(self, args: dict):
        await args["channel"].send(embed=User.getInstance().getScore(args["user"]))

    @require_role("editor")
    @log_this_async
    async def addWord(self, args: dict):
        for word in args["command"]["args"]:
            Word.getInstance().addWord(word, args["user"])

        response = f'**{"**, **".join(args["command"]["args"])}** ajouté{(len(args["command"]["args"]) > 1) * "s"}'
        await args["channel"].send(response)

    @require_role("player")
    @log_this_async
    async def listWord(self, args: dict):
        listEmbed = Word.getInstance().wordsEmbed()

        await args["channel"].send(embed=listEmbed)

    @require_role("editor")
    @log_this_async
    async def delWord(self, args: dict):
        for word in args["command"]["args"]:
            if Word.getInstance().delWord(word):
                await args["channel"].send(f"Le mot {word} a été supprimé")
            else:
                await args["channel"].send(f"Le mot {word} n'existe pas dans la liste")

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
                    await args["channel"].send(f"```{command} :\n\t{self.help[command]}```")
                else:
                    await args["channel"].send(f"Commande inconnue '{command}'")
        else:
            embed = Embed(title="Liste de commandes", color=0xFF464A)
            for command in self.commands.keys():
                if command in self.help.keys():
                    embed.add_field(name=command, value=self.help[command], inline=False)
                else:
                    embed.add_field(name=command, value="¯\\_(ツ)_/¯", inline=False)
            await args["channel"].send(embed=embed)

    @log_this_async
    async def execute(self, command):
        args = await self.parse_command(command)
        if args["command"]["command"] not in self.commands.keys():
            raise CommandNotFoundException(args["command"]["command"])
        else:
            await self.commands[args["command"]["command"]](args=args)
