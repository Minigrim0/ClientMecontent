from discord import Embed

from singleton.user import User
from src.decorators import connected


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

    @connected
    def addWord(self, word: str, user, db, cursor, scripts):
        user_id = User.getInstance().getUserID(str(user.id))
        print(user_id)
        cursor.execute(scripts["add_word"], (word, user_id))
        db.commit()

    @connected
    def listWords(self, db, cursor, scripts):
        return cursor.execute(scripts["list_words"]).fetchall()

    @connected
    def delWord(self, word: str, db, cursor, scripts):
        exists = cursor.execute("SELECT COUNT(*) FROM Words WHERE word=?", (word,)).fetchall()[0][0] == 1
        if exists:
            cursor.execute("DELETE FROM Words WHERE word=?", (word,))
            db.commit()

        return exists

    @connected
    def createGame(self, duration: int, db, cursor, scripts):
        """Adds a new game row in the database with the given duration and returns the id of this game

        Args:
            duration (int): The duration of the game to add

        Returns:
            int: the id of the added game
        """
        cursor.execute(scripts["create_game"], (duration,))
        db.commit()

        return cursor.execute("SELECT last_insert_rowid() as id").fetchall()[0][0]

    @connected
    def startGame(self, game_id: int, db, cursor, scripts):
        """Start the game with the given ID

        Args:
            game_id (int): the ID of the game to start

        Returns:
            int: the end date of the started game
        """
        cursor.execute(scripts["start_game"], (game_id,))
        db.commit()

        return cursor.execute(scripts["get_game_end"]).fetchall()[0][0]

    @connected
    def addUserToGame(self, user_id: str, game_id: str, db, cursor, scripts):
        """Add a user to a game

        Args:
            user_id (str): [description]
            game_id (str): [description]
        """
        # TODO: Check if the user is not already in the game
        cursor.execute(scripts["add_user_to_game"], (user_id, game_id, 0))
        db.commit()

    @connected
    def getParticipants(self, game_id: int, db, cursor, scripts):
        return cursor.execute(scripts["get_participants"], (game_id,)).fetchall()


    @connected
    def gameEmbed(self, game_id: int, db, cursor, scripts):
        print(self.getGameDuration(game_id=game_id))
        embed = Embed(title=f"Partie #{game_id}", color=0xff464a)
        embed.add_field(name="#Durée", value=f"{self.getGameDuration(game_id=game_id)}", inline=False)
        embed.add_field(
            name="#Partipants",
            value="\n".join(
                [f"- {user[0]}" for user in self.getParticipants(game_id=game_id)]
            ),
            inline=False
        )
        return embed
