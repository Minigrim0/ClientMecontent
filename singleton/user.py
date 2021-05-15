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
