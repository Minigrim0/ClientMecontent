from discord.ext import commands, tasks

from src.decorators import needsDatabase

from DO.game import GameDO

from singleton.game import Game


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

        self.endGameAndVotes.start()
        self.loadNearlyFinishedGamesAndVotes.start()

    @tasks.loop(seconds=1)
    async def endGameAndVotes(self):
        for game in self.nearGames:
            if game.just_ended_game:
                game.endGame()
                print("Advertising for votes")
                await Game.getInstance().showParticipations(game_id=game.id, vote=True)

        for vote in self.nearVotes:
            if vote.just_ended_vote:
                vote.endVote()
                print("Advertising for winner")
                await Game.getInstance().showParticipations(game_id=vote.id, vote=False)

    @needsDatabase
    def getNearlyEndingGames(self, db):
        """Retreive both the nearly ending games and the nearly ending votes"""
        games = db.fetch(script="get_ending_games", params=(300,))
        nearGames = []
        for game_id in games:
            game = GameDO(id=int(game_id[0])).load()
            nearGames.append(game)
        self.nearGames = nearGames

        votes = db.fetch(script="get_ending_votes", params=(300,))
        nearVotes = []
        for vote_id in votes:
            vote = GameDO(id=int(vote_id[0])).load()
            nearVotes.append(vote)
        self.nearVotes = nearVotes

    @tasks.loop(seconds=10)
    async def loadNearlyFinishedGamesAndVotes(self):
        """
        Cog task to retreive both the nearly ending games and the
        nearly ending votes
        """
        self.getNearlyEndingGames()
