import json


class Settings:
    instance = None

    @staticmethod
    def getInstance():
        if Settings.instance is None:
            Settings()
        return Settings.instance

    def __init__(self):
        if Settings.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Settings.instance = self

        with open("assets/settings.json") as settings:
            self.settings = json.load(settings)

    def __getitem__(self, item):
        return self.settings[item]
