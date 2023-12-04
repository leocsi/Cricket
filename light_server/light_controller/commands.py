from light_controller.assets.flows import *
from exceptions.light_server_exceptions import *
from yeelight.transitions import lsd, pulse
from yeelight import Flow, RGBTransition
from yeelight.flows import lsd, police

class Commands:
    def __init__(self):
        self.map = {
            "turn_on" : self.turn_on,
            "turn_off": self.turn_off,
            "toggle": self.toggle,
            "pulse": self.pulse,
            "lsd": self.lsd,
            "damage": self.damage,
            "police": self.police,
            'aurora_borealis': self.aurora_borealis
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
    
    def pulse(self):
        return 'start_flow', Flow(count=1, transitions=pulse(255, 0, 0, 50))
    
    def lsd(self):
        return 'start_flow', lsd()
    
    def damage(self):
        return 'start_flow', Flow(count=1, transitions=pulse(255, 0, 0, 50)+[RGBTransition(255,0,0,50,10),RGBTransition(255,0,0,200,100)])
    
    def police(self):
        return 'start_flow', police()
    
    def aurora_borealis(self):
        return 'start_flow', aurora_borealis()