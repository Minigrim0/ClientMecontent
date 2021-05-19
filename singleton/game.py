from discord import Embed

from src.decorators import needsDatabase
from src.exceptions import BadTypeArgumentException

from DO.user import UserDO
from DO.game import GameDO


class Game:
    instance = None

    @staticmethod
    def getInstance():
        if Game.instance is None:
            Game()
        return Game.instance

    def __init__(self):
        if Game.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Game.instance = self

    def createGame(self, duration: int):
        """Adds a new game row in the database with the given duration and returns the id of this game

        Args:
            duration (int): The duration of the game to add

        Returns:
            int: the id of the added game
        """

        if not duration.isdigit():
            raise BadTypeArgumentException(arg=duration, requiredType=int)

        game = GameDO(duration=duration)
        game.save()
        return game.id

    def startGame(self, game_id: str):
        """Start the game with the given ID

        Args:
            game_id (int): the ID of the game to start

        Returns:
            int: the end date of the started game
        """
        if not game_id.isdigit():
            raise BadTypeArgumentException(arg=game_id, requiredType=int)

        game = GameDO(id=game_id).load()

        if game.phase > 0:  # The game has started
            raise Exception("Cette partie a déjà démarré !")

        words = Word.getInstance().getRandomWords(game.nb_words)
        game.start(words=words)

        return game.end_date

    def addUserToGame(self, user_id: str, game_id: str):
        """Add a user to a game

        Args:
            user_id (str): [description]
            game_id (str): [description]
        """
        user = UserDO(id=user_id)
        game = GameDO(id=game_id)
        user.load()
        game.load()

        game.addOrRemoveUser(user, add=True)

    def removeUserFromGame(self, user_id: str, game_id: str):
        """Removes a user from a game

        Args:
            user_id (str): [description]
            game_id (str): [description]
        """
        user = UserDO(id=user_id).load()
        game = GameDO(id=game_id).load()

        game.addOrRemoveUser(user, add=False)

    def getGameDuration(self, game_id: int):
        game = GameDO(id=game_id)
        game.load()
        return game.duration

    def gameEmbed(self, game_id: str):
        if not game_id.isdigit():
            raise BadTypeArgumentException(arg=game_id, requiredType=int)

        game = GameDO(id=int(game_id))
        game.load()

        embed = Embed(title=f"Partie #{game_id}", color=0xFF464A)
        embed.add_field(name="#Paramètres", value=game.parameters, inline=True)
        embed.add_field(name="#Phase", value=game.phase_display, inline=False)
        if game.phase > 0:
            embed.add_field(name="#Date de début", value=game.start_date_display, inline=True)
            embed.add_field(name="#Date de fin", value=game.end_date_display, inline=True)
            embed.add_field(name="#Mots choisits", value=game.words, inline=True)

        participants = "\n".join([f"- {user}" for user in game.participants])
        if participants != "":
            embed.add_field(name="#Partipants", value=participants, inline=False)
        else:
            embed.add_field(name="#Partipants", value="personne lel", inline=False)

        return embed
