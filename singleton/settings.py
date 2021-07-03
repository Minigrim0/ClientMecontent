import os
import glob
import json


class Settings:
    instance = None

    @staticmethod
    def getInstance(debug=False):
        """Returns the instance of the singleton

        Returns:
            Settings: The instance
        """
        if Settings.instance is None:
            Settings(debug=debug)
        return Settings.instance

    def __init__(self, debug):
        self.debug = debug

        if Settings.instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            Settings.instance = self

        if not self.debug:
            self.load_settings()
        else:
            self.load_debug_settings()

    def load_settings(self):
        with open("assets/settings.json") as settings:
            self.settings = json.load(settings)

        self.load_scripts()

    def load_debug_settings(self):
        with open("assets/settings_debug.json") as settings:
            self.settings = json.load(settings)

        self.load_scripts()

    def load_scripts(self):
        scripts = {}
        for script in glob.glob("assets/scripts/*.sql"):
            path, filename = os.path.split(script)
            filename, ext = os.path.splitext(filename)
            with open(script) as script:
                scripts[filename] = "".join(script.readlines())
        self.settings["scripts"] = scripts

    def __getitem__(self, item):
        return self.settings[item]
