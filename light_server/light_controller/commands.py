from light_server.light_controller.assets import *
from light_server.exceptions.light_server_exceptions import *

class Commands:
    def Commands(self):
        self.map = {
            "turn_on" : self.turn_on,
        }
    def get_command_with_params(self, command):
        try:
            return self.map[command]()
        except KeyError:
            raise CommandNotFoundException(command)
    def turn_on():
        return 'turn_on'