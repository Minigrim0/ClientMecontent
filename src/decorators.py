import traceback
import logging
import sys

from src.utils import send_error_message


class require_role:
    """
    A decorator verifying that the user that wrote the command as the rights to execute this command
    """

    def __init__(self, *authorized_roles):
        self.authorized_roles = authorized_roles

    def __call__(self, *args, **kwargs):
        func = args[0]

        async def wrapper(*args, **kwargs):
            # TODO: Check the user's roles
            await func(*args, **kwargs)

        return wrapper  # (*args, **kwargs)


def log_this_async(func):
    """
    A decorator to log eventual errors occuring in the code
    """

    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            await send_error_message(kwargs, e)
            logging.error(f"Error occured in {func.__name__} : {e}")
            error_type, error, tb = sys.exc_info()
            error_msg = "".join(traceback.format_exception(error_type, error, tb))
            logging.error(error_msg)

    return wrapper


def connected(func):
    """A decorator wrapping a sql connection to a database
    """
    def wrapper(*args, **kwargs):
        db = sqlite3.connect(databaseLocation())
        cursor = db.cursor()
        kwargs["db"] = db
        kwargs["cursor"] = cursor
        result = func(*args, **kwargs)
        db.close()
        return result

    return wrapper
