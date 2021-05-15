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
    def addUser(self, user, db, cursor):
        cursor.execute(
            "INSERT INTO Users (username, discord_id, score) VALUES (?, ?, ?)", (user.name, str(user.id), 0)
        )
        db.commit()
        return cursor.execute("SELECT last_insert_rowid()").fetchall()[0]
