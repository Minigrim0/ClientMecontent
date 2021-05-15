
from src.decorators import connected


class Database:
    instance = None

    @staticmethod
    def getInstance():
        if Database.instance is None:
            Database()
        return Database.instance

    @connected
    def __init__(self, db, cursor):
        if Database.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Database.instance = self

        with open("assets/init_db.sql", "r") as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)
        db.commit()
