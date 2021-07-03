from discord import Embed

from src.exceptions import (
    BadTypeArgumentException,
    InvalidFieldException,
    InvalidArgumentException,
    IllegalUserException,
)

from src.utils import convert_mention_to_id

from DO.user import UserDO
from DO.game import GameDO

from singleton.word import Word
from singleton.client import Bot


class Game:
    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            Game: The instance
        """
        if Game.instance is None:
            Game()
        return Game.instance

    def __init__(self):
        if Game.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Game.instance = self

    def createGame(self, parameters: list, user_id):
        """Adds a new game row in the database with the given duration and returns the id of this game

        Args:
            duration (int): The duration of the game to add

        Returns:
            int: the id of the added game
        """

        if len(parameters) == 0:
            game = GameDO()
            game.save(reload=False)
        else:
            game_duration = parameters[0]
            if not game_duration.isdigit():
                raise BadTypeArgumentException(arg=game_duration, requiredType=int)

            game = GameDO(game_duration=game_duration)
            game.save(reload=False)

        user = UserDO(id=user_id).load()
        game.addOrRemoveUser(user, add=True)
        game.setHost(user)
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

    def modGame(self, game_id: str, user_id: int, field: str, value):
        """Modifies the given parameter to the given value

        Args:
            game_id (str): the id of the game on which to modify the parameter
            user_id (int): the id of the user who made the modification
            field (str): The filed to modify
            value (?): The new value

        Raises:
            BadTypeArgumentException: In case the argument has a bad type
            PermissionError: In case the user does not have the permission to run this command on this game
            InvalidFieldException: In case the field is not recognised
        """
        if not game_id.isdigit():
            raise BadTypeArgumentException(arg=game_id, requiredType=int)
        game = GameDO(id=int(game_id)).load()
        if user_id != game.host:
            raise PermissionError("Tu n'as pas la permission de faire ceci !")

        fields = ["host", "game_duration", "vote_duration", "nb_words"]
        if field not in fields:
            raise InvalidFieldException(field, possibleFields=fields)

        if field == "host":
            self.modHost(game, value)
        elif field == "nb_words":
            self.modWords(game, value)
        else:
            self.modDuration(game, field, value)

    def modHost(self, game: GameDO, user: str):
        user_id = convert_mention_to_id(user)
        if not user_id.isdigit():
            raise InvalidArgumentException(user, "mention d'un utilisateur")

        user = UserDO(id=user_id).load()
        if game.id not in user.games:
            raise IllegalUserException(user_id, game.id)

        game.setHost(user)

    def modDuration(self, game, field, value):
        if not value.isdigit():
            raise BadTypeArgumentException("caractères", requiredType="nombre")

        game.modDuration(value, gameDuration=(field == "game_duration"))

    def modWords(self, game, value):
        if not value.isdigit():
            raise BadTypeArgumentException("caractères", requiredType="nombre")

        game.modWordsAmount(int(value))

    def addUserToGame(self, user_id: str, game_id: str):
        """Add a user to a game

        Args:
            user_id (str): [description]
            game_id (str): [description]
        """
        user = UserDO(id=user_id).load()
        game = GameDO(id=game_id).load()

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
        """Returns the duration of a game

        Args:
            game_id (int): The id of the game to get the duration of

        Returns:
            int: the duration of the game in seconds
        """
        game = GameDO(id=game_id).load()
        return game.duration

    def submit(self, game_id: str, user_id: str, artwork_url: str, artwork_title: str):
        if not game_id.isdigit():
            raise BadTypeArgumentException(arg=game_id, requiredType=int)
        game = GameDO(id=int(game_id)).load()
        if game.phase == 0:
            raise Exception("La partie n'a pas encore commencé, vous ne pouvez pas encore envoyer de proposition")

        game.addSubmission(user_id, artwork_title, artwork_url)

    def vote(self, game_id: str, user_id: str, participation_id: str):
        if not game_id.isdigit():
            raise BadTypeArgumentException(arg=game_id, requiredType=int)
        game = GameDO(id=int(game_id)).load()
        user = UserDO(id=int(user_id)).load()

        if game.phase != 2:
            raise Exception("Cette partie n'est pas en phase de vote !")
        if int(participation_id) > len(game.artworks):
            raise Exception(f"L'ID de participation n'est pas bon (max: {len(game.artworks)})")

        participation = game.artworks[int(participation_id)-1]
        if participation.user_id == user_id:
            raise Exception("Tu ne peux pas voter pour toi même !")
        if user.votedFor(game_id):
            raise Exception("Tu as déjà voté pour cette partie !")

        game.addVote(user_id, participation.id)

    def gameEmbed(self, game_id: str):
        if not game_id.isdigit():
            raise BadTypeArgumentException(arg=game_id, requiredType=int)

        game = GameDO(id=int(game_id)).load()

        embed = Embed(title=f"Partie #{game_id} ({game.phase_display})", color=game.color)
        embed.add_field(name="#Paramètres", value=game.parameters, inline=True)
        if game.phase > 0:
            embed.add_field(name="#Mots choisits", value=game.words_display, inline=True)
            embed.add_field(name="#Date de début", value=game.start_date_display, inline=True)
            if game.phase == 1:
                embed.add_field(name="#Temps de jeu restant", value=game.time_left, inline=True)
            elif game.phase == 2:
                embed.add_field(name="#Temps de vote restant", value=game.time_left, inline=True)
            else:
                embed.add_field(name="#Date de fin", value=game.end_date_display, inline=True)
            embed.add_field(name="#Participations", value=game.participations_display, inline=True)

        embed.add_field(name="#Partipants", value=game.participants_display, inline=False)

        return embed

    async def showParticipations(self, game_id: str, vote: bool = True):
        game = GameDO(id=game_id).load()

        if vote:
            channel = Bot.getInstance().getChannel("votes")
        else:
            channel = Bot.getInstance().getChannel("participations")

        for index, artwork in enumerate(game.artworks):
            await channel.send(embed=await artwork.asEmbed(game_id=game_id, index=index+1, revealAuthor=not vote))
