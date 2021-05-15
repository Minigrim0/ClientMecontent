from src.decorators import connected


class Game:
    instance = None

    @staticmethod
    def getInstance():
        if Game.instance is None:
            Game()
        return Game.instance

    @connected
    def __init__(self, db, cursor):
        if Game.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Game.instance = self

        with open("assets/init_db.sql", "r") as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)
        db.commit()

    @connected
    def addWord(self, word: str, user, db, cursor):
        user_id = cursor.execute("SELECT ID FROM Users WHERE discord_id=?", (str(user.id),)).fetchall()
        if len(user_id) == 0:
            user_id = self.addUser(user)
        else:
            user_id = user_id[0][0]

        print(user_id)
        cursor.execute("INSERT INTO Words (word, creator_id) VALUES (?, ?)", (word, user_id))
        db.commit()

    @connected
    def listWords(self, db, cursor):
        words = cursor.execute(
            "SELECT word, users.username FROM Words LEFT JOIN Users ON Words.creator_id=Users.id"
        ).fetchall()
        return words

    @connected
    def delWord(self, word: str, db, cursor):
        cursor.execute("DELETE FROM Words WHERE word=?", (word,))
        db.commit()

    def startGame(self):
        pass

    @connected
    def addUser(self, user, db, cursor):
        cursor.execute(
            "INSERT INTO Users (username, discord_id, score) VALUES (?, ?, ?)", (user.name, str(user.id), 0)
        )
        db.commit()
        return cursor.execute("SELECT last_insert_rowid()").fetchall()[0]

    def addUserToGame(self, user_id: str, game_id: str):
        pass
