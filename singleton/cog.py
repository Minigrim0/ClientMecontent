from discord.ext import commands, tasks


class GameCog(commands.Cog):
    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton
        
        Returns:
            GameCog: The instance
        """
        if GameCog.instance is None:
            GameCog()
        return GameCog.instance

    def __init__(self):
        if GameCog.instance is not None:
            raise Exception("This class is a singleton !")
        GameCog.instance = self

        self.nearGames = []
        self.nearVotes = []

    @tasks.loop(seconds=1)
    async def endGameAndVotes(self):
        for game in self.nearGames:
            if game.justEnded():
                await game.voteTime()

        for vote in self.nearVotes:
            if vote.justEnded():
                await vote.showScore()

    @tasks.loop(seconds=30)
    def loadNearlyFinishedGamesAndVotes(self):
        pass
