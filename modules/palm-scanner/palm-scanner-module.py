import transitions
from enum import Enum, auto

from ProximitySensor import ProximitySensor

class States(str, Enum):
    IDLE = 'IDLE'
    DETECTING = 'DETECTING'
    SCANNING = 'SCANNING'

class Events(str, Enum):
    enableProxSensor = 'enableProxSensor'
    detectHand = 'detectHand'
    reset = 'reset'

class PalmReader:

    proximitySensor = ProximitySensor()
    
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
    
    def on_enter_DETECTING(self):
        def onDetect():
            self.trigger(Events.detectHand)            
        self.proximitySensor.startDetect(onDetect)
    


palmReader = PalmReader()