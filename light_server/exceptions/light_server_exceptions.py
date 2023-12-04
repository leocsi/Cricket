class CommandNotFoundException(Exception):
    def __init__(self, command, message="Could not recognize command: "):
        self.command = command
        self.message = message
        super().__init__(self.message + self.command)

class ColorCreationException(Exception):
    def __init__(self, args: dict, message):
        self.args = list(args.keys())
        self.message = message
        super().__init__("Could not create color with argument(s)" + str(self.args) + self.message)