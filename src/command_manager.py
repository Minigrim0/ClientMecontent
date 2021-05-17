import re
import random

from discord import Embed
from discord.utils import get

from src.decorators import log_this_async, require_role, require_parameters
from src.exceptions import CommandNotFoundException, BadFormatException, BadTypeArgumentException

from singleton.settings import Settings
from singleton.game import Game
from singleton.user import User

from src.utils import gameEmbed


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
        }
        self.help = Settings.getInstance()["help"]

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

    @require_role("player")
    @require_parameters(1)
    @log_this_async
    async def newGame(self, args: dict):
        duration = args["command"]["args"][0]
        if not duration.isdigit():
            raise BadTypeArgumentException(arg=duration, requiredType=int)
        game_id = Game.getInstance().createGame(duration)
        user_id = User.getInstance().getUserID(args["user"].id)
        Game.getInstance().addUserToGame(user_id, game_id)
        participants = Game.getInstance().getParticipants(game_id)

        embed = gameEmbed(gameID=game_id, duration=duration, participants=participants)
        await args["channel"].send(embed=embed)

    @require_role("player")
    @require_parameters(1)
    @log_this_async
    async def startGame(self, args: dict):
        pass

    @log_this_async
    async def register(self, args: dict):
        if not User.getInstance().exists(args['user']):
            User.getInstance().addUser(args["user"])
            role = get(args["guild"].roles, id=int(Settings.getInstance()["roles"]["player"]))
            await args["user"].add_roles(role)
            await args["channel"].send("Tu es maintenant un photographe !")
        else:
            await args["channel"].send("Tu es déjà enregistré !")

    @require_role("player")
    @log_this_async
    async def getScore(self, args: dict):
        score = User.getInstance().getScore(args["user"])

        embed = Embed(title=f"Profil de {args['user'].name}", color=0xff464a)
        embed.set_thumbnail(url=args['user'].avatar_url)
        embed.add_field(name="#score", value=f"{score['score']}", inline=True)
        embed.add_field(name="#victoires", value=f"{score['victories']}", inline=True)
        embed.add_field(name="#participations", value=f"{score['participations']}", inline=True)
        await args["channel"].send(embed=embed)

    @require_role("editor")
    @log_this_async
    async def addWord(self, args: dict):
        for word in args["command"]["args"]:
            Game.getInstance().addWord(word, args["user"])

        response = f'**{"**, **".join(args["command"]["args"])}** ajouté{(len(args["command"]["args"]) > 1) * "s"}'
        await args["channel"].send(response)

    @require_role("player")
    @log_this_async
    async def listWord(self, args: dict):
        wordList = Game.getInstance().listWords()
        maxLength = max([len(word[0]) for word in wordList])
        response = ""

        for word, user in wordList:
            response += f"{word.ljust(maxLength)} | {user}\n"

        response = f"Liste des mots :\n```\n{response}```"

        await args["channel"].send(response)

    @require_role("editor")
    @log_this_async
    async def delWord(self, args: dict):
        for word in args["command"]["args"]:
            if Game.getInstance().delWord(word):
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
                    await args["channel"].send(f'```{command} :\n\t{self.help[command]}```')
                else:
                    await args["channel"].send(f"Commande inconnue '{command}'")
        else:
            embed = Embed(title="Liste de commandes", color=0xff464a)
            for command in self.commands.keys():
                embed.add_field(name=command, value=self.help[command], inline=False)
            await args["channel"].send(embed=embed)

    @log_this_async
    async def execute(self, command):
        args = await self.parse_command(command)
        if args["command"]["command"] not in self.commands.keys():
            raise CommandNotFoundException(args["command"]["command"])
        else:
            await self.commands[args["command"]["command"]](args=args)
