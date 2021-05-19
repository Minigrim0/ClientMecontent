from src.decorators import needsDatabase


class GameDO:
    """Handles database fetching and update for game objects"""

    def __init__(self, id=None, phase=0, start_date=None, end_date=None, duration=0):
        self.id = id
        self.phase = phase
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration

        self.participants = []

        self.phases = ["enregistrement", "partie en cours", "votes en cours", "partie terminée"]

    @needsDatabase
    def save(self, db):
        """Save the game object to the database"""
        if self.duration is None:
            raise Exception("Impossible de sauvegarder la partie sans sa durée !")

        if self.id is not None:
            db.update(
                script="upd_game",
                params=(self.id, self.phase, self.duration),
            )
        else:
            self.id = db.update(script="add_game", params=(self.duration,))

    @needsDatabase
    def load(self, db):
        """Loads information from the database"""
        if self.id is None:
            raise Exception("Impossible de charger une partie sans son id !")

        data = db.fetch(script="get_game", params=(self.id,))[0]

        self.id = data[0]
        self.registration_phase = data[1]
        self.finished = data[2]
        self.start_date = data[3]
        self.end_date = data[4]
        self.duration = data[5]
