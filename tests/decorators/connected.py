import os
import glob
import sqlite3


def connected(func):
    """A test decorator wrapping a sql connection to a database
    """
    def wrapper(*args, **kwargs):
        scripts = {}
        for script in glob.glob("assets/scripts/*.sql"):
            path, filename = os.path.split(script)
            filename, ext = os.path.splitext(filename)
            with open(script) as script:
                scripts[filename] = "".join(script.readlines())
        scripts

        if os.path.isfile("assets/photo_debug.db"):
            os.remove("assets/photo_debug.db")
        db = sqlite3.connect("assets/photo_debug.db")
        cursor = db.cursor()
        cursor.executescript(scripts["init_db"])

        kwargs["db"] = db
        kwargs["cursor"] = cursor
        kwargs["scripts"] = scripts
        result = func(*args, **kwargs)
        os.remove("assets/photo_debug.db")
        db.close()
        return result

    return wrapper
