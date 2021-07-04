from discord import Embed, Member

from DO.user import UserDO


class User:
    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            User: The instance
        """
        if User.instance is None:
            User()
        return User.instance

    def __init__(self):
        if User.instance is not None:
            raise Exception("This class is a singleton!")
        else:
            User.instance = self

    def addUser(self, user: Member):
        UserDO(id=user.id, username=user.name).save()

    def exists(self, user: Member):
        return UserDO(id=user.id).load().username is not None

    def getScore(self, discord_user):
        user = UserDO(id=discord_user.id).load()

        embed = Embed(title=f"Profil de {user.username}", color=0xFF464A)
        embed.set_thumbnail(url=discord_user.avatar_url)
        embed.add_field(name="#score", value=f"{user.score}", inline=True)
        embed.add_field(name="#victoires", value=f"{user.victories}", inline=True)
        embed.add_field(name="#participations", value=f"{user.participations}", inline=True)

        return embed
