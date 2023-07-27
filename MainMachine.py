import transitions
from enum import Enum

class States(str, Enum):
    ADDING_CREDIT = 'ADDING_CREDIT'
    FETCHING_FORTUNE = 'FETCHING_FORTUNE'
    READING_FORTUNE =  'READING_FORTUNE'


class Events(str, Enum):
    toFetchingFortune = 'toFetchingFortune'
    toReadingFortune = 'toReadingFortune'
    reset = 'reset'

class MainMachine:

    credit = 0

    def __init__(self) -> None:

        stateTransitions = [
            [Events.toFetchingFortune, States.ADDING_CREDIT, States.FETCHING_FORTUNE],
            [Events.toReadingFortune, States.FETCHING_FORTUNE,States.READING_FORTUNE],
            [Events.reset, States.READING_FORTUNE,States.ADDING_CREDIT,],
            ]
        
        self.machine = transitions.Machine(
            model=self,
            states=States,
            transitions=stateTransitions,
            initial=States.ADDING_CREDIT
            )
        
        self.on_enter_ADDING_CREDIT()
    
    def onAddCredit(self, newCredit):
        print('onAddCredit:', newCredit)
        self.credit += newCredit

        # AUDIO ############################
        # MAYBE: comment on added coin ("2 euros, wow", "10 cents, you cheap")
        print('onAddCredit: AUDIO: sound Ka$hinggg')


        # PALM SCANNER ############################
        # palmScanner.setState('DETECTING_PALM')
        print("onAddCredit: palmScanner.setState('DETECTING_PALM')")

    def onDetectPalm(self):
        print("onDetectPalm: transition to FETCHING_FORTUNE")
        self.toFetchingFortune()

    def onReceiveGptOracleFortune(self):
        print("onReceiveGptOracleFortune: create TTS mp3 file")
        print("onReceiveGptOracleFortune: transition to READING_FORTUNE")
        self.toReadingFortune()

    def onCompleteFortuneReading(self):
        print('onCompleteFortuneReading')
        self.reset()

    def on_enter_ADDING_CREDIT(self):
        print('')
        # AUDIO ############################
        # play soft mystical music
        # MAYBE: play "cat calls" (calling customers)
        print('on_enter_ADDING_CREDIT: AUDIO: play soft mystical music')

        
        # MOTOR ############################
        # blow bubbles very sporadicly
        print('on_enter_ADDING_CREDIT: MOTOR: blow bubbles very sporadicly')


        # PALM SCANNER ############################
        # if has credit:
        #   palmScanner.setState('DETECTING_PALM')
        # else:
        #   palmScanner.setState('FLICKERING')
        print("on_enter_ADDING_CREDIT: PALM SCANNER: palmScanner.setState('DETECTING_PALM') or palmScanner.setState('FLICKERING')")

    def on_enter_FETCHING_FORTUNE(self):
        print('')
        # AUDIO ############################
        # play elevator music
        print("on_enter_ADDING_CREDIT: AUDIO: play elevator music")

        # GPT ORACLE ############################
        # self.gptOracle.requestFortune()
        #   - on success
        #       -> self.setFortuneText()
        #       -> self.toReadingFortune()
        #   - on error -> MAYBE read some kind of backup fortune?
        print("on_enter_ADDING_CREDIT: GPT ORACLE: gptOracle.requestFortune()")

        # MOTOR ############################
        # blow bubbles sporadicly
        print('on_enter_ADDING_CREDIT: MOTOR: blow bubbles sporadicly')


        # PALM SCANNER ############################
        # palmScanner.setState('SCANNING')
        print("on_enter_ADDING_CREDIT: PALM SCANNER: palmScanner.setState('SCANNING')")
    
    def on_enter_READING_FORTUNE(self):
        print('')

        # AUDIO ############################
        # play intense mystical music
        print("on_enter_READING_FORTUNE: AUDIO: play intense mystical music")
        
        # Text To Speech, then:
        # play fortune reading mp3:
        #   - on complete -> self.reset()

        # PALM SCANNER ############################
        # Nothing! (Still in 'SCANNING' state)


# Modules:
# Audio
# Coin Acceptor
# Lcd Display
# Bubble Motor
# Palm Scanner
# NeoPixel Manager (Motor + Scanner leds)
# Gpt Oracle (ChatGPT Client)
