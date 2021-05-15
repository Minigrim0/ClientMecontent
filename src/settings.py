import json


class Settings:
    instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Settings.instance == None:
            Settings()
        return Settings.instance

    def __init__(self):
        """ Virtually private constructor. """
        if Settings.instance != None:
            raise Exception("This class is a Settings!")
        else:
            Settings.instance = self
        
        with open("assets/settings.json") as settings:
            self.settings = json.load(settings)

    def __getitem__(self, item):
        return self.settings[item]
