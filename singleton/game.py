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
        user_id = cursor.execute("SELECT ID FROM Users WHERE discord_id=?", (str(user.id),)).fetchall()

        cursor.execute("INSERT INTO Words (word, creator_id) VALUES (?, ?)", (word, user_id))
        db.commit()

    @connected
    def listWords(self, db, cursor, scripts):
        words = cursor.execute(
            "SELECT word, users.username FROM Words LEFT JOIN Users ON Words.creator_id=Users.id"
        ).fetchall()
        return words

    @connected
    def delWord(self, word: str, db, cursor, scripts):
        exists = cursor.execute("SELECT COUNT(*) FROM Words WHERE word=?", (word,)).fetchall()[0][0] == 1
        if exists:
            cursor.execute("DELETE FROM Words WHERE word=?", (word,))
            db.commit()

        return exists

    def startGame(self):
        pass

    def addUserToGame(self, user_id: str, game_id: str):
        pass
