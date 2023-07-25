import transitions
from enum import Enum
from modules.coin_acceptor.CoinAcceptor import CoinAcceptor
from modules.lcd_display.LcdDisplay import LcdDisplay
from modules.palm_reader.PalmReader import PalmReader

class States(str, Enum):
    IDLE = 'IDLE'
    ADDING_CREDIT = 'ADDING_CREDIT'
    WAITING_PALM =  'WAITING_PALM'
    READING_FORTUNE = 'READING_FORTUNE'

class Events(str, Enum):
    toNext = 'toNext'
    x = 'x'
    reset = 'reset'

class FortunerTeller:

    credit = 0
    
    def __init__(self) -> None:

        self.coinAcceptor = CoinAcceptor(self.addCredit)
        self.palmReader = PalmReader(self.onDetectPalmCallback)
        self.lcdDisplay = LcdDisplay()

        stateTransitions = [
            [Events.toNext, States.IDLE, States.ADDING_CREDIT],
            [Events.toNext, States.ADDING_CREDIT,States.WAITING_PALM],
            [Events.toNext, States.WAITING_PALM,States.READING_FORTUNE,],
            [Events.reset,States.READING_FORTUNE,States.IDLE]
            ]

        self.machine = transitions.Machine(
            model=self,
            states=States,
            transitions=stateTransitions,
            initial=States.IDLE
            )
        
        self.on_enter_IDLE()
    
    def on_enter_IDLE(self):
        self.lcdDisplay.writeLine1('-> Pay $$$')
        self.lcdDisplay.writeLine2('-> Get Fortune')

    def addCredit(self, newCredit):
        self.credit += newCredit

        self.lcdDisplay.writeLine1(f'Money$: {self.credit}')
        self.lcdDisplay.writeLine2('')
    
    def on_enter_ADDING_CREDIT(self):
        self.coinAcceptor.enable()
        self.lcdDisplay.writeLine1('Add coins to')
        self.lcdDisplay.writeLine2('start...')

    def on_exit_ADDING_CREDIT(self):
        self.coinAcceptor.disable()
    
    def on_enter_WAITING_PALM(self):
        self.palmReader.enableProxSensor()

    def onDetectPalmCallback(self):
        self.toNext()
        self.palmReader.detectHand()
    
    def on_exit_READING_FORTUNE(self):
        self.credit = 0
        self.palmReader.reset()

fortunerTeller = FortunerTeller()