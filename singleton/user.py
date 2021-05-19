from discord import Embed

from src.decorators import needsDatabase

from DO.user import UserDO


class User:
    instance = None

    @staticmethod
    def getInstance():
        if User.instance is None:
            User()
        return User.instance

    def __init__(self):
        if User.instance is not None:
            raise Exception("This class is a singleton!")
        else:
            User.instance = self

    @needsDatabase
    def getUserID(self, discordID: str, db):
        return db.fetch(script="get_user_id", params=(discordID,))[0][0]

    @needsDatabase
    def addUser(self, user, db):
        return db.update(script="add_user", params=(user.id, user.name, 0))

    @needsDatabase
    def exists(self, user, db):
        return db.fetch(script="user_exists", params=(user.id,))[0][0]

    def getScore(self, discord_user):
        user = UserDO(id=discord_user.id)
        user.load()

        embed = Embed(title=f"Profil de {user.username}", color=0xFF464A)
        embed.set_thumbnail(url=discord_user.avatar_url)
        embed.add_field(name="#score", value=f"{user.score}", inline=True)
        embed.add_field(name="#victoires", value=f"{user.victories}", inline=True)
        embed.add_field(name="#participations", value=f"{user.participations}", inline=True)

        return embed
