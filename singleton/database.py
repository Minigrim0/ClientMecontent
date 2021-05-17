
from src.decorators import connected


class Database:
    instance = None

    @staticmethod
    def getInstance():
        if Database.instance is None:
            Database()
        return Database.instance

    @connected
    def __init__(self, db, cursor, scripts):
        if Database.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Database.instance = self

        cursor.executescript(scripts["init_db"])
        db.commit()
