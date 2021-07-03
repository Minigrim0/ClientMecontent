import datetime

from singleton.settings import Settings


async def send_error_message(decorator_kwargs: dict, error_msg: str):
    """Sends a message with the informations on the error that occured

    Args:
        decorator_kwargs (dict): The kwargs of the decorator  calling this function
        error_msg (str): The message to display
    """
    if type(decorator_kwargs) is dict:
        if "command" in decorator_kwargs.keys():
            channel = decorator_kwargs["command"].channel
        else:
            channel = decorator_kwargs["args"]["channel"]
    else:
        return

    await channel.send(error_msg)


def databaseLocation():
    """Returns the location of the database file"""
    return Settings.getInstance()["database"]["location"]


def secondsToHMS(seconds: int):
    """Transformas an amount of seconds in HMS format

    Args:
        seconds (int): The amount of seconds to transform

    Returns:
        str: The HMS format of the seconds
    """
    return str(datetime.timedelta(seconds=seconds))


def getDiffElements(initialList: list, newList: list) -> list:
    """Returns the elements that differ in the two given lists

    Args:
        initialList (list): The first list
        newList (list): The second list

    Returns:
        list: The list of element differing between the two given lists
    """
    final = []
    for element in newList:
        if element not in initialList:
            final.append(element)

    return final
