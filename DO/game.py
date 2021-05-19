import pytz
import datetime

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

    @property
    def start_date_display(self):
        if self.start_date is not None:
            return (
                datetime.datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
                .replace(tzinfo=pytz.utc)
                .astimezone(tz=pytz.timezone("Europe/Brussels"))
                .strftime("%d-%m-%Y %H:%M:%S")
            )
        return "$Error$"

    @property
    def end_date_display(self):
        if self.end_date is not None:
            return (
                datetime.datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
                .replace(tzinfo=pytz.utc)
                .astimezone(tz=pytz.timezone("Europe/Brussels"))
                .strftime("%d-%m-%Y %H:%M:%S")
            )
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

        return self

    @needsDatabase
    def start(self, db):
        if self.id is None:
            raise Exception("Impossible de démarrer une partie sans id !")

        db.update(script="start_game", params=(self.id,))
        self.load()

    @needsDatabase
    def addOrRemoveUser(self, user, db, add=True):
        if add:
            if int(self.id) in user.games:
                raise Exception("Tu participe déjà à cette partie !")

            db.update(script="add_user_to_game", params=(user.id, self.id, 0))
        else:
            if int(self.id) not in user.games:
                raise Exception("Tu ne participe pas à cette partie !")

            db.update(script="remove_user_from_game", params=(user.id, self.id))
