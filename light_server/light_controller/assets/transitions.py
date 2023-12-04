import numpy as np
import random

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


class TransitionModifiers:
    @staticmethod
    def randomDurations(transitions: 'list[FlowTransition]', duration_unit: int=3000) ->'list[FlowTransition]':
        n_transitions = len(transitions)
        intervals = np.random.random(n_transitions)
        total_length = duration_unit * n_transitions

        intervals /= intervals.sum()
        intervals *= total_length


        for e, i in enumerate(intervals):
            diff = 750 - i
            if diff > 0:
                longest_i = np.where(intervals == np.max(intervals))
                np.put(intervals, longest_i, intervals[longest_i] - diff)
                np.put(intervals, e, i+ diff)
        for i in range(n_transitions):
            transitions[i].set_duration(intervals[i])
        
        return transitions
    
    @staticmethod
    def shuffleTransitions(transitions: 'list[FlowTransition]') ->'list[FlowTransition]':
        random.shuffle(transitions)
        return transitions


transitions = [
    TemperatureTransition(1700)
]

def transitionSuiteFromPalette(palette_name: str) -> list[ColorTransition]:
    return [ColorTransition(color.color) for color in ColorStore.get_palette(palette_name)]
