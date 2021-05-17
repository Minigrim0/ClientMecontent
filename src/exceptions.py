class CommandNotFoundException(Exception):
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return f"the command '{self.command}' could not be found, type !help for help"


class BadFormatException(Exception):
    def __init__(self, command: str, pattern: str):
        self.command = command
        self.pattern = pattern

    def __str__(self):
        return (
            f"the command '{self.command}' does not follow the pattern '{self.pattern}'"
        )


class BadTypeArgumentException(Exception):
    def __init__(self, arg, requiredType):
        self.arg = arg
        self.requiredType = requiredType

    def __str__(self):
        return (
            f"L'argument {self.arg} n'a pas le bon type (Requis : {self.requiredType}, recu {type(self.arg)})"
        )
