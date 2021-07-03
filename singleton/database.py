from src.decorators import connected


class Database:
    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            Database: The instance
        """
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
        print("Executing FETCH :\n", scripts[script], "\nwith parameters", params)
        return cursor.execute(scripts[script], params).fetchall()

    @connected
    def update(self, db, cursor, scripts, script: str, params=tuple()):
        """Execute a script in order to fetch data from the database

        Args:
            script (str): the name of the script to execute

        Returns:
            int: the id of the newly inserted_row
        """
        print("Executing UPDATE :\n", scripts[script], "\nwith parameters", params)
        cursor.execute(scripts[script], params)
        db.commit()
        return cursor.execute("SELECT last_insert_rowid()").fetchall()[0][0]
