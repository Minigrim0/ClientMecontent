import pytz
import emoji
import datetime

from src.decorators import needsDatabase
from src.exceptions import BadTypeArgumentException
import src.utils as utils

from DO.user import UserDO


class GameDO:
    """Handles database fetching and update for game objects"""

    def __init__(
        self, id=None, phase=0, start_date=None, end_date=None, game_duration=3600, vote_duration=600, nb_words=3
    ):
        self.id = id
        self.phase = phase
        self.start_date = start_date
        self.end_date = end_date
        self.game_duration = game_duration
        self.vote_duration = vote_duration
        self.nb_words = nb_words
        self.host = None

        self.words = []
        self.participants = []

        self.phases = ["Enregistrement", "En cours", "Votes en cours", "Partie terminée"]

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

    @property
    def parameters(self):
        parameters = f"Durée du jeu : {utils.secondsToHMS(self.game_duration)}\n"
        parameters += f"Durée des votes : {utils.secondsToHMS(self.vote_duration)}\n"
        parameters += f"Nombre de mots : {self.nb_words}\n"
        return parameters

    @property
    def words_display(self):
        return "\n".join([f"- {word}" for word in self.words])

    @property
    def participants_display(self):
        display = ""
        for user in self.participants:
            display += f"- {user[0]}"
            if user[1] == self.host:
                display += f" {emoji.emojize(':crown:')}"
            display += "\n"
        return display

    @needsDatabase
    def setWords(self, words, db):
        if self.words != []:
            raise Exception("Les mots choisits ne peuvent pas être modifiés !")

        self.words = words
        for word in self.words:
            db.update(script="add_word_to_game", params=(word.id, self.id))

    @needsDatabase
    def save(self, db, reload=True):
        """Save the game object to the database"""
        if self.id is not None:
            db.update(
                script="upd_game",
                params=(self.id, self.phase, self.game_duration),
            )
        else:
            self.id = db.update(script="add_game", params=(self.game_duration,))
        if reload:
            self.load()

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
        self.game_duration = data[4]
        self.vote_duration = data[5]
        self.nb_words = data[6]

        self.participants = db.fetch(script="get_participants", params=(self.id,))
        if len(self.participants) == 0:
            self.delete()
            raise Exception(f"Tous les joueurs ont quitté la partie #{self.id}. Supression...")

        self.words = [word[0] for word in db.fetch(script="get_game_words", params=(self.id,))]
        host = db.fetch(script="get_game_host", params=(self.id,))
        if len(host) == 0:  # Set a user host if no user is host
            self.setHost(UserDO(id=self.participants[0][1]))
        else:
            self.host = host[0][0]

        return self

    @needsDatabase
    def delete(self, db):
        if self.id is None:
            raise Exception("Impossible de supprimer une partie sans son id !")

        db.update(script="del_game", params=(self.id,))

    @needsDatabase
    def setHost(self, user, db):
        db.update(script="del_game_hosts", params=(self.id,))
        db.update(script="add_game_host", params=(self.id, user.id))
        self.host = user.id

    @needsDatabase
    def start(self, words, db):
        if self.id is None:
            raise Exception("Impossible de démarrer une partie sans id !")

        db.update(script="start_game", params=(self.id,))
        self.setWords(words)
        self.load()

    @needsDatabase
    def addOrRemoveUser(self, user, db, add=True):
        if self.phase > 0:
            raise Exception("Il n'est plus possible de joindre ou quitter cette partie !")

        if add:
            if int(self.id) in user.games:
                raise Exception("Tu participe déjà à cette partie !")

            db.update(script="add_user_to_game", params=(user.id, self.id, 0))
        else:
            if int(self.id) not in user.games:
                raise Exception("Tu ne participe pas à cette partie !")

            db.update(script="remove_user_from_game", params=(user.id, self.id))

            self.load()

    @needsDatabase
    def modDuration(self, value, db, gameDuration=True):
        if self.phase > 0:
            raise Exception("Il n'est plus possible de modifier les paramètres cette partie !")

        params = (value, self.id)
        if gameDuration:
            script = "upd_game_duration"
        else:
            script = "upd_vote_duration"

        db.update(script=script, params=params)
        self.load()
