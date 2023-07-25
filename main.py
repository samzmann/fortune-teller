import transitions
from enum import Enum
from modules.coin_acceptor.CoinAcceptor import CoinAcceptor

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
    
    def on_enter_ADDING_CREDIT(self):
        self.coinAcceptor.enable()

    def on_exit_ADDING_CREDIT(self):
        self.coinAcceptor.disable()
    
    def on_exit_READING_FORTUNE(self):
        self.credit = 0

fortunerTeller = FortunerTeller()