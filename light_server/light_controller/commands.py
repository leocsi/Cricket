from light_controller.assets.flows import *
from exceptions.light_server_exceptions import *
from yeelight.transitions import lsd, pulse
from yeelight import Flow, RGBTransition
from yeelight.flows import lsd, police

class Commands:

    @staticmethod
    def turn_on():
        return 'turn_on:0:0', None
    
    @staticmethod
    def turn_off():
        return 'turn_off:0:0', None
    
    @staticmethod
    def toggle():
        return 'toggle:0:0', None
    
    @staticmethod
    def pulse():
        return 'start_flow:0:0', Flow(count=1, transitions=pulse(255, 0, 0, 50))
    
    @staticmethod
    def lsd():
        return 'start_flow:0:0', lsd()
    
    @staticmethod
    def damage():
        return 'start_flow:0:0', Flow(count=1, transitions=pulse(255, 0, 0, 50)+[RGBTransition(255,0,0,50,10),RGBTransition(255,0,0,200,100)])
    
    @staticmethod
    def police():
        return 'start_flow:0:0', police()
    
    @staticmethod
    def aurora_borealis():
        return 'start_flow:1:0', aurora_borealis()

    MAP = {
        "turn_on:" : turn_on,
        "turn_off": turn_off,
        "toggle": toggle,
        "pulse": pulse,
        "lsd": lsd,
        "damage": damage,
        "police": police,
        'aurora_borealis': aurora_borealis
    }

    @staticmethod
    def get_command_with_params(command):
        try:
            return Commands.MAP[command]()
        except KeyError:
            raise CommandNotFoundException(command)

class CommandContext:
    def __init__(self, name):
        self.name = name
        self.command, self.flow = Commands.get_command_with_params(name)

        self.command = self.parse_execution_mode(self.command)
    
    def parse_execution_mode(self, command):
        command_components = command.split(':')
        command_name = command_components[0]
        command_modes = command_components[1:]

        attributes = ['trueRandom', 'stateful']
        for i, attr in enumerate(attributes):
            if i >= len(command_modes):
                self.__setattr__(attr, False)
            else:
                self.__setattr__(attr, bool(int(command_modes[i])))

        return command_name
    
    def new_flow(self):
        if not self.trueRandom:
            raise Exception()
        _, self.flow = Commands.get_command_with_params(self.name)