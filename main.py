import transitions
from enum import Enum
from modules.coin_acceptor.CoinAcceptor import CoinAcceptor
from modules.lcd_display.LcdDisplay import LcdDisplay

class States(str, Enum):
    IDLE = 'IDLE'
    ADDING_CREDIT = 'ADDING_CREDIT'
    READING_FORTUNE = 'READING_FORTUNE'

class Events(str, Enum):
    toAddingCredit = 'toAddingCredit'
    toReadingFortune = 'toReadingFortune'
    reset = 'reset'

class FortunerTeller:

    credit = 0
    
    def __init__(self) -> None:

        self.coinAcceptor = CoinAcceptor(self.addCredit)
        self.lcdDisplay = LcdDisplay()

        stateTransitions = [
            [Events.toAddingCredit, States.IDLE, States.ADDING_CREDIT],
            [Events.toReadingFortune, States.ADDING_CREDIT,States.READING_FORTUNE,],
            [Events.reset,States.READING_FORTUNE,States.IDLE]
            ]

        self.machine = transitions.Machine(
            model=self,
            states=States,
            transitions=stateTransitions,
            initial=States.IDLE
            )

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
    
    def on_exit_READING_FORTUNE(self):
        self.credit = 0

fortunerTeller = FortunerTeller()