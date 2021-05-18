from discord import Embed

from src.decorators import needsDatabase


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
        return db.update(script="add_user", params=(user.name, str(user.id), 0))

    @needsDatabase
    def exists(self, user, db):
        return db.fetch(script="user_exists", params=(user.id,))[0][0]

    @needsDatabase
    def getGames(self, user_id: int, db):
        games = db.fetch(script="get_user_games", params=(user_id,))
        return [game[0] for game in games]

    @needsDatabase
    def getScore(self, user, db):
        score = db.fetch(script="user_score", params=(user.id,))[0][0]
        victories = db.fetch(script="victories", params=(user.id,))[0][0]
        participations = db.fetch(script="participations", params=(user.id,))[0][0]

        embed = Embed(title=f"Profil de {user.name}", color=0xFF464A)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="#score", value=f"{score}", inline=True)
        embed.add_field(name="#victoires", value=f"{victories}", inline=True)
        embed.add_field(name="#participations", value=f"{participations}", inline=True)

        return embed
