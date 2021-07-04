from src.decorators import needsDatabase

from DO.vote import VoteDO


class UserDO:
    """Handles database fetching and update for User objects"""

    def __init__(self, id: int = None, username: str = None):
        self.id = id
        self.username = username
        self.games = []
        self.victories = 0
        self.participations = 0
        self.votes = []

    @needsDatabase
    def save(self, db):
        """Saves the user to the database"""
        if self.id is None:
            raise Exception("Le champ id ne peut pas être vide")

        self.id = db.update(script="add_user", params=(self.id, self.username))

    @needsDatabase
    def load(self, db):
        """loads a user from the database"""
        if self.id is None:
            raise Exception("Impossible de charger un utilisateur sans son id !")

        data = db.fetch(script="get_user", params=(self.id,))

        if len(data) != 0:
            self.id, self.username, _ = data[0]

            self.games = [game[0] for game in db.fetch(script="get_user_games", params=(self.id,))]
            self.victories = db.fetch(script="get_user_victories", params=(self.id,))[0][0]
            self.participations = db.fetch(script="get_user_participations", params=(self.id,))[0][0]

        votes = db.fetch(script="get_user_votes", params=(int(self.id),))
        for vote in votes:
            game_id, artwork_id = vote
            self.votes.append(VoteDO(self.id, int(game_id), int(artwork_id)))

        return self

    def votedFor(self, game_id: int):
        for vote in self.votes:
            if vote.game_id == game_id:
                return True
        return False

    @property
    def score(self):
        return sum([self.game_score(game_id) for game_id in self.games])

    @needsDatabase
    def game_score(self, game_id: int, db) -> int:
        return db.fetch(script="get_artwork_vote", params=(self.id, game_id))[0][0]

    def delete(self, db):
        pass
