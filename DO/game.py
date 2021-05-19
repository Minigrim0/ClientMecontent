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

    @property
    def phase_display(self):
        if 0 <= self.phase < len(self.phases):
            return self.phases[self.phase]
        return "$Error$"

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
        self.phase = data[1]
        self.start_date = data[2]
        self.end_date = data[3]
        self.duration = data[4]

        participants = db.fetch(script="get_participants", params=(self.id,))
        self.participants = [user[0] for user in participants]

    @needsDatabase
    def start(self, db):
        if self.id is None:
            raise Exception("Impossible de démarrer une partie sans id !")

        db.update(script="start_game", params=(self.id,))
        self.load()
