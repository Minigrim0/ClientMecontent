class CommandNotFoundException(Exception):
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return "the cpmmand {self.command} could not be found, type !help for help"
