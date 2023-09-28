class CommandNotFoundException(Exception):
    def __init__(self, command, message="Could not recognize command: "):
        self.command = command
        self.message = message
        super().__init__(self.message + self.command)
