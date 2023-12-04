
from yeelight.flow import Flow, Action, FlowTransition

from light_controller.assets.transitions import *

def aurora_borealis() -> Flow:
    transitions = transitionSuiteFromPalette('aurora_borealis')
    transitions = TransitionModifiers.randomDurations(transitions)
    transitions = TransitionModifiers.shuffleTransitions(transitions)

    return Flow(0, Action.recover, transitions=transitions)

