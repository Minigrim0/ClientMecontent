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

    @connected
    def fetch(self, db, cursor, scripts, script: str, params=tuple()):
        """Execute a script in order to fetch data from the database

        Args:
            script (str): the name of the script to execute
        """
        return cursor.execute(scripts[script], params).fetchall()

    @connected
    def update(self, db, cursor, scripts, script: str, params=tuple()):
        """Execute a script in order to fetch data from the database

        Args:
            script (str): the name of the script to execute
        """
        cursor.execute(scripts[script], params)
        db.commit()
