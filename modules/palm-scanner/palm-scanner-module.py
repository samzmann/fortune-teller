import transitions
from enum import Enum, auto

from ProximitySensor import ProximitySensor
from ScannerLeds import ScannerLeds

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
    scannerLeds = ScannerLeds()
    
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
  
    def on_exit_IDLE(self):
        self.scannerLeds.stopAnim()
    
    def on_exit_DETECTING(self):
        self.scannerLeds.stopAnim()
    
    def on_exit_SCANNING(self):
        self.scannerLeds.stopAnim()
    
    # Will automatically trigger when the machine enters DETECTING state
    def on_enter_DETECTING(self):
        self.scannerLeds.startBreathAnim()

        def onDetect():
            self.trigger(Events.detectHand)            
        self.proximitySensor.startDetect(onDetect)
    
    def on_enter_SCANNING(self):
        self.scannerLeds.startScanAnim()


palmReader = PalmReader()