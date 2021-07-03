import re

from discord import Embed
from discord.utils import get

from src.decorators import log_this_async, require_role, require_parameters, require_channel
from src.exceptions import (
    CommandNotFoundException, BadFormatException, MissingAttachementException)

from singleton.settings import Settings
from singleton.game import Game
from singleton.user import User
from singleton.word import Word


class CommandManager:
    def __init__(self, client):
        self.client = client
        self.commands = {
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
            "mod": self.modGame,
            "submit": self.submit
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
            "initial_command": command
        }

    @require_parameters(2)
    @require_channel(inGuild=False)
    @log_this_async
    async def submit(self, args):
        if len(args["initial_command"].attachments) != 1:
            raise MissingAttachementException(1)
        artwork_url = args["initial_command"].attachments[0].url
        game_id, artwork_title = args["command"]["args"]
        Game.getInstance().submit(game_id, args["user"].id, artwork_url, artwork_title)

        await args["channel"].send("Ta participation a bien été enregistrée")

    @require_role("player")
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def newGame(self, args: dict):
        game_id = Game.getInstance().createGame(args["command"]["args"], args["user"].id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=str(game_id)))

    @require_parameters(1)
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def gameInfo(self, args: dict):
        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=args["command"]["args"][0]))

    @require_parameters(1)
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def joinGame(self, args: dict):
        game_id = args["command"]["args"][0]
        Game.getInstance().addUserToGame(args["user"].id, game_id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=game_id))

    @require_parameters(3)
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def modGame(self, args: dict):
        game_id, field, value = args["command"]["args"]
        Game.getInstance().modGame(game_id, args["user"].id, field, value)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=game_id))

    @require_parameters(1)
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def leaveGame(self, args: dict):
        game_id = args["command"]["args"][0]
        Game.getInstance().removeUserFromGame(args["user"].id, game_id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=game_id))

    @require_role("player")
    @require_parameters(1)
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def startGame(self, args: dict):
        game_id = args["command"]["args"][0]
        Game.getInstance().startGame(game_id=game_id)

        await args["channel"].send(embed=Game.getInstance().gameEmbed(game_id=game_id))

    @require_channel(inGuild=True, channels=["bot"])
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
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def getScore(self, args: dict):
        await args["channel"].send(embed=User.getInstance().getScore(args["user"]))

    @require_role("editor")
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def addWord(self, args: dict):
        for word in args["command"]["args"]:
            Word.getInstance().addWord(word, args["user"])

        response = f'**{"**, **".join(args["command"]["args"])}** ajouté{(len(args["command"]["args"]) > 1) * "s"}'
        await args["channel"].send(response)

    @require_role("player")
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def listWord(self, args: dict):
        listEmbed = Word.getInstance().wordsEmbed()

        await args["channel"].send(embed=listEmbed)

    @require_role("editor")
    @require_channel(inGuild=True, channels=["bot"])
    @log_this_async
    async def delWord(self, args: dict):
        for word in args["command"]["args"]:
            if Word.getInstance().delWord(word):
                await args["channel"].send(f"Le mot {word} a été supprimé")
            else:
                await args["channel"].send(f"Le mot {word} n'existe pas dans la liste")

    @require_channel(inGuild=True, channels=["bot"])
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
