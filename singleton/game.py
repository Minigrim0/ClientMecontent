from discord import Embed

from src.decorators import needsDatabase


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

    @needsDatabase
    def createGame(self, duration: int, db):
        """Adds a new game row in the database with the given duration and returns the id of this game

        Args:
            duration (int): The duration of the game to add

        Returns:
            int: the id of the added game
        """

        if not duration.isdigit():
            raise BadTypeArgumentException(arg=duration, requiredType=int)

        return db.update(script="create_game", params=(duration,))

    @needsDatabase
    def startGame(self, game_id: int, db):
        """Start the game with the given ID

        Args:
            game_id (int): the ID of the game to start

        Returns:
            int: the end date of the started game
        """
        db.update(script="start_game", params=(game_id,))

        return db.fetch(script="get_game_end")[0][0]

    @needsDatabase
    def addUserToGame(self, user_id: str, game_id: str, db):
        """Add a user to a game

        Args:
            user_id (str): [description]
            game_id (str): [description]
        """
        # TODO: Check if the user is not already in the game
        db.update(script="add_user_to_game", params=(user_id, game_id, 0))

    @needsDatabase
    def getParticipants(self, game_id: int, db):
        return db.fetch(script="get_participants", params=(game_id,))

    @needsDatabase
    def getGameDuration(self, game_id: int, db):
        return db.fetch(script="get_game_duration", params=(game_id,))[0][0]

    @needsDatabase
    def gameEmbed(self, game_id: int, db):
        print(self.getGameDuration(game_id=game_id))
        embed = Embed(title=f"Partie #{game_id}", color=0xFF464A)
        embed.add_field(name="#Durée", value=f"{self.getGameDuration(game_id=game_id)}", inline=False)
        embed.add_field(
            name="#Partipants",
            value="\n".join([f"- {user[0]}" for user in self.getParticipants(game_id=game_id)]),
            inline=False,
        )
        return embed
