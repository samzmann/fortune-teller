import transitions
from enum import Enum, auto

class States(str, Enum):
    IDLE = 'IDLE'
    DETECTING = 'DETECTING'
    SCANNING = 'SCANNING'

class Events(str, Enum):
    enableProxSensor = 'enableProxSensor'
    detectHand = 'detectHand'
    reset = 'reset'

class PalmReader:
    
    def __init__(self) -> None:

        stateTransitions = [
            [Events.enableProxSensor, States.IDLE, States.DETECTING],
            [Events.detectHand, States.DETECTING,States.SCANNING,],
            [Events.reset,States.SCANNING,States.IDLE]
            ]

        self.machine = transitions.Machine(
            model=self,
            states=States,
            transitions=stateTransitions,
            initial=States.IDLE
            )

palmReader = PalmReader()