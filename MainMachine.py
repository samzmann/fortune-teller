import transitions
from enum import Enum

from modules.bubble_motor.BubbleMotor import BubbleMotor
from modules.coin_acceptor.CoinAcceptor import CoinAcceptor
from modules.lcd_display.LcdDisplay import LcdDisplay
from modules.neopixel_manager.NeopixelManager import NeopixelManager, NeopixelCommands
from modules.palm_reader.ProximitySensor import ProximitySensor


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

        # self.bubbleMotor = BubbleMotor()
        self.coinAcceptor = CoinAcceptor(self.onAddCredit)
        self.lcdDisplay = LcdDisplay()
        self.neopixelManager = NeopixelManager()
        self.proximitySensor = ProximitySensor()

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

        # LCD ############################
        if self.is_ADDING_CREDIT():
            print(f'onAddCredit: LCD: show credit {self.credit}')
            self.lcdDisplay.writeLine1(f'Credit: {self.credit}')
            self.lcdDisplay.writeLine2('')
        else:
            print(f'onAddCredit: LCD: Credit for next reading: {self.credit}')
            self.lcdDisplay.writeLine1('Credit for next')
            self.lcdDisplay.writeLine2(f'reading: {self.credit}')

        # PALM SCANNER ############################
        print("onAddCredit: PALM SCANNER: proximitySensor.startDetect()")
        self.proximitySensor.startDetect(self.onDetectPalm)
        self.neopixelManager.send(NeopixelCommands.SCANNER_BREATH_GREEN)

    def onDetectPalm(self):
        if self.credit == 0:
            print("onDetectPalm: No credit. Ignoring")
            return
        print("onDetectPalm: transition to FETCHING_FORTUNE")
        self.toFetchingFortune()

    def onReceiveGptOracleFortune(self):
        print("onReceiveGptOracleFortune: create temp TTS mp3 file")
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
        # self.bubbleMotor.runVerySporadic()
        self.neopixelManager.send(NeopixelCommands.MOTOR_RAINBOW)

        # LCD ############################
        if self.credit > 0:
            print(f'on_enter_ADDING_CREDIT: LCD: show credit {self.credit}')
            self.lcdDisplay.writeLine1(f'Credit: {self.credit}')
            self.lcdDisplay.writeLine2('')
        else:
            print('on_enter_ADDING_CREDIT: LCD: Add coins to start...')
            self.lcdDisplay.writeLine1('Add coins to')
            self.lcdDisplay.writeLine2('start...')


        # PALM SCANNER ############################
        if self.credit > 0:
            print("on_enter_ADDING_CREDIT: PALM SCANNER: proximitySensor.startDetect()")
            self.proximitySensor.startDetect(self.onDetectPalm)
            self.neopixelManager.send(NeopixelCommands.SCANNER_BREATH_GREEN)
        else:
            print("on_enter_ADDING_CREDIT: PALM SCANNER flicker")
            self.neopixelManager.send(NeopixelCommands.SCANNER_FLICKER)

    def on_enter_FETCHING_FORTUNE(self):
        print('')
        # AUDIO ############################
        # play elevator music
        print("on_enter_ADDING_CREDIT: AUDIO: play elevator music")

        # GPT ORACLE ############################
        # self.gptOracle.requestFortune(self.credit) AND then reset self.credit
        #   - on success
        #       -> self.setFortuneText()
        #       -> self.toReadingFortune()
        #   - on error -> MAYBE read some kind of backup fortune? (eg. useBackupFortune(self.credit))
        print(f"on_enter_ADDING_CREDIT: GPT ORACLE: gptOracle.requestFortune({self.credit})")

        # LCD ############################
        print(f'on_enter_FETCHING_FORTUNE: LCD: You have nice nails!')
        self.lcdDisplay.writeLine1('You have nice')
        self.lcdDisplay.writeLine2('hands :/')

        # MOTOR ############################
        # self.bubbleMotor.runSporadic()
        print('on_enter_ADDING_CREDIT: MOTOR: blow bubbles sporadicly')


        # PALM SCANNER ############################
        print("on_enter_ADDING_CREDIT: PALM SCANNER SCANNER_SCAN")
        self.neopixelManager.send(NeopixelCommands.SCANNER_SCAN)
    
    def on_enter_READING_FORTUNE(self):
        print('')

        # AUDIO ############################
        # play intense mystical music
        print("on_enter_READING_FORTUNE: AUDIO: play intense mystical music")
        # play TTS mp3 file
        print("on_enter_READING_FORTUNE: AUDIO: play TTS mp3 file")
        
        # Text To Speech, then:
        # play fortune reading mp3:
        #   - on complete -> self.reset()

        # LCD ############################
        print(f'on_enter_READING_FORTUNE: LCD: Your destiny...')
        self.lcdDisplay.writeLine1('Your destiny')
        self.lcdDisplay.writeLine2('is here!')

        # PALM SCANNER ############################
        # Nothing! (Still in 'SCANNING' state)

    def on_exit_READING_FORTUNE(self):
        # AUDIO ############################
        # delete temp TTS mp3 file
        print("on_exit_READING_FORTUNE: AUDIO: delete temp TTS mp3 file")

m = MainMachine()

# Modules:
# Audio
# Coin Acceptor
# Lcd Display
# Bubble Motor
# Palm Scanner
# NeoPixel Manager (Motor + Scanner leds)
# Gpt Oracle (ChatGPT Client)
