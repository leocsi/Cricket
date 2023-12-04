from yeelight.flow import *
from light_controller.assets.colors import *

class ColorTransition(FlowTransition):
    def __init__(self, color, duration=300, brightness=100):
        self.color = color
        self.duration = duration
        self.brightness = brightness

        self._mode = 1

    def set_duration(self, time: int):
        self.duration = time
    @property
    def _value(self):
        return self.color
    
    def __repr__(self):
        return "<%s value %s duration %s, brightness %s>" % (
            self.__class__.__name__,
            self._value,
            self.duration,
            self.brightness,
        )

transitions = [
    TemperatureTransition(1700)
]

def transitionSuiteFromPalette(palette_name: str) -> list[ColorTransition]:
    return [ColorTransition(color.color) for color in ColorStore.get_palette(palette_name)]
