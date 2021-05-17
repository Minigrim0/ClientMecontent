from discord import Embed

from singleton.settings import Settings


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


def gameEmbed(gameID: int, duration: int, participants: list):
    embed = Embed(title=f"Partie #{gameID}", color=0xff464a)
    embed.add_field(name="#Durée", value=f"{duration}", inline=False)
    embed.add_field(name="#Partipants", value="\n".join([f"- {user[0]}" for user in participants]), inline=False)
    return embed
