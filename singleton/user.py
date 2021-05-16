from src.decorators import connected


class User:
    instance = None

    @staticmethod
    def getInstance():
        if User.instance is None:
            User()
        return User.instance

    def __init__(self):
        if User.instance is not None:
            raise Exception("This class is a singleton!")
        else:
            User.instance = self

    @connected
    def addUser(self, user, db, cursor):
        cursor.execute(
            "INSERT INTO Users (username, discord_id, score) VALUES (?, ?, ?)", (user.name, str(user.id), 0)
        )

        db.commit()
        return cursor.execute("SELECT last_insert_rowid()").fetchall()[0][0]

    @connected
    def exists(self, user, db, cursor):
        return cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE discord_id=?", (user.id,)
        ).fetchall()[0][0] > 0

    @connected
    def getScore(self, user, db, cursor):
        score = cursor.execute(
            "SELECT score FROM Users WHERE discord_id=?", (user.id,)
        ).fetchall()[0][0]

        victories = cursor.execute(
            "SELECT COUNT(*) FROM (SELECT userToGame.user_id as winner_id FROM Game LEFT JOIN userToGame ON userToGame.game_id = Game.id AND userToGame.votes=(SELECT MAX(votes) FROM userToGame WHERE game_id=Game.id)) WHERE winner_id = ?", (user.id,)
        ).fetchall()[0][0]

        participations = cursor.execute(
            "SELECT COUNT(*) FROM userToGame WHERE user_id = ?", (user.id,)
        ).fetchall()[0][0]

        return locals()
