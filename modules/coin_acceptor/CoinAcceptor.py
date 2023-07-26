import transitions
from enum import Enum
import RPi.GPIO as GPIO
from threading import Timer

class States(str, Enum):
    DISABLED = 'DISABLED'
    ENABLED = 'ENABLED'

class Events(str, Enum):
    enable = 'enable'
    disable = 'disable'

class CoinAcceptor:
    
    LAST_IMPULSE_TIMEOUT = 0.150 # 150 ms
    numImpulses = 0
    totalAmount = 0

    timerObj = None

    def __init__(self, onAddCredit) -> None:

        self.onAddCredit = onAddCredit

        COIN_PIN = 21 # Physical Pin 40
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(COIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(COIN_PIN, GPIO.FALLING)
        GPIO.add_event_callback(COIN_PIN, self.onPulseReceived)

        stateTransitions = [
            [Events.enable, States.DISABLED, States.ENABLED],
            [Events.disable, States.ENABLED, States.DISABLED]
            ]

        self.machine = transitions.Machine(
            model=self,
            states=States,
            transitions=stateTransitions,
            initial=States.DISABLED
            )

    def registerImpulses(self):

        increment = 0
        if (self.numImpulses == 1):
            increment = 1 # 1 Euro coin
            print("1 Euro")
        elif (self.numImpulses == 2):
            increment = 0.5 # 50 Cents coin
            print("50 Cents")

        self.numImpulses = 0
        self.onAddCredit(increment)

    def onPulseReceived(self, pin):
        print('onPulseReceived')

        # # Ignore pulses if CoinAcceptor is not enabled
        # if self.is_ENABLED() == False:
        #     print('pulse ignore because CoinAcceptor disabled')
        #     return

        if self.timerObj != None and self.timerObj.is_alive:
                self.timerObj.cancel()

        self.numImpulses += 1
        
        self.timerObj = Timer(
            self.LAST_IMPULSE_TIMEOUT,
            self.registerImpulses)
        
        self.timerObj.start()
          
def onAddCredit(c):
    print('onAddCredit', c)

c = CoinAcceptor(onAddCredit)