class InstructionResolver:
    def __init__(self):
        self.simple=["toggle"]
        self.map = {
            "lights off" : ["turn_off"],
            "toggle" : ["toggle"]
        }

    def get_command_suite(self, command: str):
        if command in self.simple:
            return [command]
        return self.map[command]