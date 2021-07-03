import sqlite3
import traceback
import logging
from datetime import datetime
import sys

from src.utils import send_error_message, databaseLocation
from singleton.settings import Settings
from singleton.client import Bot


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
            arguments = kwargs["args"]["command"]["args"]

            if len(arguments) == self.nb_parameters:
                await func(*args, **kwargs)
            else:
                await kwargs["args"]["channel"].send(
                    f"Ta commande n'a pas le bon nombre de paramètres ! (Requis: {self.nb_parameters})"
                )

        return wrapper  # (*args, **kwargs)


class require_channel:
    """A decorator checking the place the command has been made in"""

    def __init__(self, inGuild: bool = True, channels: list = []):
        self.in_guild = inGuild

        if len(channels) > 0:
            channels = [Settings.getInstance()["channels"][channel] for channel in channels]
        self.channels = channels

    @property
    def good_channels(self):
        bot = Bot.getInstance()
        msg = ""
        for channel in self.channels:
            channel = bot.get_channel(int(channel))
            msg += channel.mention + ", "
        return msg[:-2]

    def __call__(self, *args, **kwargs):
        func = args[0]

        async def wrapper(*args, **kwargs):
            isInGuild = kwargs["args"]["guild"] is not None
            channel = kwargs["args"]["channel"]

            if isInGuild == self.in_guild:
                if self.in_guild and len(self.channels) > 0 and str(channel.id) not in self.channels:
                    await kwargs["args"]["initial_command"].delete()
                    await kwargs["args"]["channel"].send(
                        f"Cette commande ne peut pas être effectuée dans ce channel ! (Channel(s) autorisé(s): {self.good_channels})"
                    )
                else:
                    await func(*args, **kwargs)
            else:
                required = "Message Privé" if isInGuild else "Serveur"
                await kwargs["args"]["initial_command"].delete()
                await kwargs["args"]["channel"].send(
                    f"Cette command ne peut pas être effectuée dans ce channel ! (Requis: {required})"
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
