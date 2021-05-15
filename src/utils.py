from src.settings import Settings


async def send_error_message(decorator_kwargs, error_msg: str):
    if type(decorator_kwargs) is dict:
        if "command" in decorator_kwargs.keys():
            channel = decorator_kwargs["command"].channel
        else:
            channel = decorator_kwargs["args"]["channel"]
    else:
        return

    await channel.send(error_msg)


def databaseLocation():
    """Returns the location of the database file
    """
    return Settings.getInstance()["database"]["location"]
