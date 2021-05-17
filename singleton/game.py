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
    def startGame(self, duration: int, db, cursor, scripts):
        """Adds a new game row in the database with the given duration and returns the id of this game

        Args:
            duration (int): The duration of the game to add

        Returns:
            int: the id of the added game
        """
        cursor.execute(scripts["create_game"], (duration,))
        db.commit()

        return cursor.execute("SELECT last_insert_rowid() as id").fetchall()[0][0]


    def addUserToGame(self, user_id: str, game_id: str):
        pass
