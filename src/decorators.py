import traceback
import logging
import sys

import asyncio


class require_role:
    """
    A decorator verifying that the user that wrote the command as the rights to execute this command
    """

    def __init__(self, func=None, *authorized_roles):
        self.func = func
        self.authorized_roles = authorized_roles

    def __call__(self, *args, **kwargs):
        print("In require role :", args, kwargs)
        if not self.func:
            return self.__class__(args[0], authorized_roles=self.authorized_roles)

        async def wrapper(*args, **kwargs):
            if len(args[0]) >= self.nb_parameters:
                await self.func(*args, **kwargs)
            else:
                await args[1].send("T'as pas le droit !")

        return wrapper(*args, **kwargs)


def log_this(func):
    """
    A decorator to log eventual errors occuring in the code
    """
    if asyncio.iscoroutinefunction(func):

        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logging.error(f"Error occured in {func.__name__} : {e}")
                error_type, error, tb = sys.exc_info()
                error_msg = "".join(traceback.format_exception(error_type, error, tb))
                logging.error(error_msg)

        return wrapper

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f'Error occured in "{func.__name__}" : {e}')
            error_type, error, tb = sys.exc_info()
            error_msg = "".join(traceback.format_exception(error_type, error, tb))
            logging.error(error_msg)

    return wrapper
