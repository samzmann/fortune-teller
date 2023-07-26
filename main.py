import transitions
from enum import Enum
from modules.bubble_motor.BubbleMotor import BubbleMotor
from modules.coin_acceptor.CoinAcceptor import CoinAcceptor
from modules.lcd_display.LcdDisplay import LcdDisplay
from modules.palm_reader.PalmReader import PalmReader

class States(str, Enum):
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

        self.bubbleMotor = BubbleMotor()
        self.coinAcceptor = CoinAcceptor(self.addCredit)
        self.lcdDisplay = LcdDisplay()
        self.palmReader = PalmReader(self.onDetectPalmCallback)

        stateTransitions = [
            [Events.toNext, States.ADDING_CREDIT,States.WAITING_PALM],
            [Events.toNext, States.WAITING_PALM,States.READING_FORTUNE,],
            [Events.reset,States.READING_FORTUNE,States.ADDING_CREDIT]
            ]

        self.machine = transitions.Machine(
            model=self,
            states=States,
            transitions=stateTransitions,
            initial=States.ADDING_CREDIT
            )
        
        self.on_enter_ADDING_CREDIT()
    
    # def on_enter_IDLE(self):
    #     self.lcdDisplay.writeLine1('-> Pay $$$')
    #     self.lcdDisplay.writeLine2('-> Get Fortune')

    def addCredit(self, newCredit):
        self.credit += newCredit

        self.lcdDisplay.writeLine1(f'Money$: {self.credit}')
        self.lcdDisplay.writeLine2('')
        self.bubbleMotor.runSporadic()
    
    def on_enter_ADDING_CREDIT(self):
        self.bubbleMotor.stopRun()
        self.palmReader.pause()
        self.palmReader.enableProxSensor()
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