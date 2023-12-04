import numpy as np
import random

from yeelight.flow import Flow, Action, FlowTransition

from light_controller.assets.transitions import *

class TransitionModifiers:
    @staticmethod
    def randomDurations(transitions: 'list[FlowTransition]', duration_unit: int=3000) ->'list[FlowTransition]':
        n_transitions = len(transitions)
        intervals = np.random.random(n_transitions)
        total_length = duration_unit * n_transitions

        intervals /= intervals.sum()
        intervals *= total_length
        
        for i in range(n_transitions):
            transitions[i].set_duration(intervals[i])
        
        return transitions
    
    @staticmethod
    def shuffleTransitions(transitions: 'list[FlowTransition]') ->'list[FlowTransition]':
        random.shuffle(transitions)
        return transitions


def aurora_borealis() -> Flow:
    transitions = transitionSuiteFromPalette('aurora_borealis')
    transitions = TransitionModifiers.randomDurations(transitions)
    transitions = TransitionModifiers.shuffleTransitions(transitions)

    return Flow(0, Action.recover, transitions=transitions)

