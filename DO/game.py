class GameDO:
    """Handles database fetching and update for game objects"""

    def __init__(self, id=None, registration_phase=True, finished=False, start_date=None, end_date=None, duration=0):
        self.id = id
        self.registration_phase = registration_phase
        self.finished = finished
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration

    def save(self):
        """Save the game object to the database"""
        pass

    def load(self):
        """Loads information from the database"""
        pass
