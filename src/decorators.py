import sqlite3
import traceback
import logging
from datetime import datetime
import sys

from src.utils import send_error_message, databaseLocation
from singleton.settings import Settings


class require_role:
    """A decorator verifying that the user that wrote the command as the rights to execute this command"""

    def __init__(self, *authorized_roles):
        self.authorized_roles = [Settings.getInstance()["roles"][role] for role in authorized_roles]

    def __call__(self, *args, **kwargs):
        func = args[0]

        async def wrapper(*args, **kwargs):
            user = kwargs["args"]["user"]

            if any(str(role.id) in set(self.authorized_roles) for role in user.roles):
                await func(*args, **kwargs)
            else:
                await kwargs["args"]["channel"].send("Tu n'as pas la permission de faire ceci !")

        return wrapper  # (*args, **kwargs)


class require_parameters:
    """A decorator checking that the amount of parameters is correct for the command to work"""

    def __init__(self, nb_parameters):
        self.nb_parameters = nb_parameters

    def __call__(self, *args, **kwargs):
        func = args[0]

        async def wrapper(*args, **kwargs):
            args = kwargs["args"]["command"]["args"]

            if len(args) == self.nb_parameters:
                await func(*args, **kwargs)
            else:
                await kwargs["args"]["channel"].send(
                    f"Ta commande n'a pas le bon nombre de paramètres ! (Requis: {self.nb_parameters})"
                )

        return wrapper  # (*args, **kwargs)


def log_this_async(func):
    """A decorator to log eventual errors occuring in the code"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await send_error_message(kwargs, e)
            logging.error(
                f"\n\n*** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ***\nError occured in {func.__name__} : {e}"
            )
            error_type, error, tb = sys.exc_info()
            error_msg = "".join(traceback.format_exception(error_type, error, tb))
            logging.error(error_msg)

    return wrapper


def connected(func):
    """A decorator wrapping a sql connection to a database"""

    def wrapper(*args, **kwargs):
        db = sqlite3.connect(databaseLocation())
        cursor = db.cursor()
        kwargs["db"] = db
        kwargs["cursor"] = cursor
        kwargs["scripts"] = Settings.getInstance()["scripts"]
        result = func(*args, **kwargs)
        db.close()
        return result

    return wrapper


def needsDatabase(func):
    """A decorator wrapping a sql connection to a database"""
    from singleton.database import Database

    def wrapper(*args, **kwargs):
        db = sqlite3.connect(databaseLocation())
        kwargs["db"] = Database.getInstance()
        result = func(*args, **kwargs)
        db.close()
        return result

    return wrapper
