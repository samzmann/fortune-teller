import transitions
from enum import Enum

from .ProximitySensor import ProximitySensor
from .ScannerLeds import ScannerLeds

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
    
    def __init__(self, onDetectPalm) -> None:

        self.onDetectPalm = onDetectPalm

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
    
        # Must call the on_enter_IDLE callback manually because it does not fire on Machine init
        self.on_enter_IDLE()
  
    def on_exit_IDLE(self):
        self.scannerLeds.stopAnim()
    
    def on_exit_DETECTING(self):
        self.scannerLeds.stopAnim()
    
    def on_exit_SCANNING(self):
        self.scannerLeds.stopAnim()
    
    def on_enter_IDLE(self):
        self.scannerLeds.startFlickerAnim()

    def on_enter_DETECTING(self):
        self.scannerLeds.startBreathAnim()
        self.proximitySensor.startDetect(self.onDetectPalm)
    
    def on_enter_SCANNING(self):
        self.scannerLeds.startScanAnim()