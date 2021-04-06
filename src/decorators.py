import logging
import discord

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


class log_this:
    """
        A decorator to log eventual errors occuring in the code
    """
    def __init__(self, func=None):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("In log this :", args, kwargs)
        if not self.func:
            return self.__class__(args[0])

        if asyncio.iscoroutinefunction(self.func):
            async def wrapper(*args, **kwargs):
                try:
                    result = await self.func(*args, **kwargs)
                    return result
                except Exception as e:
                    logging.error(f"Error occured in {self.func.__name__} : {e}")
                    logging.error(e.__traceback__)

            return wrapper(*args, **kwargs)
        def wrapper(*args, **kwargs):
            try:
                result = self.func(*args, **kwargs)
                return result
            except Exception as e:
                logging.error(f"Error occured in {self.func.__name__} : {e}")
                logging.error(e.__traceback__)

        return wrapper(*args, **kwargs)

    @property
    def __name__(self):
        if self.func:
            return self.func.__name__
        return self.__class__.__name__
