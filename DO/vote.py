from src.decorators import needsDatabase


class VoteDO:
    def __init__(self, user_id: int, game_id: int, artwork_id: int):
        self.user_id = id
        self.game_id = game_id
        self.artwork_id = None

    @needsDatabase
    def load(self, db):
        self.artwork_id = db.fetch(script="get_votes", params=(self.user_id, self.game_id))[0][0]
        return self
