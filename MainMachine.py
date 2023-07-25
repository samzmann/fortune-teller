import transitions
from enum import Enum

class States(str, Enum):
    ACCEPTING_CREDIT = 'ACCEPTING_INITIAL_CREDIT'
    CREDIT_COUNTDOWN = 'CREDIT_COUNTDOWN'
    WAITING_PALM =  'WAITING_PALM'
    SCANNING_PALM = 'SCANNING_PALM'


class Events(str, Enum):
    toNext = 'toNext'
    reset = 'reset'

class MainMachine:

    credit = 0

    def __init__(self) -> None:

        stateTransitions = [
            [Events.toNext, States.ACCEPTING_CREDIT, States.CREDIT_COUNTDOWN],
            [Events.toNext, States.CREDIT_COUNTDOWN,States.WAITING_PALM,],
            [Events.toNext, States.CREDIT_COUNTDOWN,States.WAITING_PALM,],
            [Events.toNext, States.WAITING_PALM,States.SCANNING_PALM,],
            [Events.reset,States.SCANNING_PALM,States.ACCEPTING_CREDIT]
            ]
        
        self.machine = transitions.Machine(
            model=self,
            states=States,
            transitions=stateTransitions,
            initial=States.ACCEPTING_CREDIT
            )
    
    def addCredit(self, newCredit):
        self.credit += newCredit

        