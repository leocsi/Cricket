from light_controller.assets import *
from exceptions.light_server_exceptions import *

class Commands:
    def __init__(self):
        self.map = {
            "turn_on" : self.turn_on,
            "turn_off": self.turn_off,
            "toggle": self.toggle
        }
    def get_command_with_params(self, command):
        try:
            return self.map[command]()
        except KeyError:
            raise CommandNotFoundException(command)
        
    def turn_on(self):
        return 'turn_on', None
    
    def turn_off(self):
        return 'turn_off', None
    
    def toggle(self):
        return 'toggle', None
    