import RPi.GPIO as GPIO
from threading import Timer
# from lcd import drivers

# display = drivers.Lcd()
# display.lcd_display_string(f"Add coins to", 1)
# display.lcd_display_string(f"start", 2)

class CoinAcceptor:
    
    LAST_IMPULSE_TIMEOUT = 0.150 # 150 ms
    numImpulses = 0
    totalAmount = 0

    timerObj = None

    def __init__(self) -> None:

        COIN_PIN = 21 # Physical Pin 40
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(COIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(COIN_PIN, GPIO.FALLING)
        GPIO.add_event_callback(COIN_PIN, self.onPulseReceived)

    def registerImpulses(self):

        if (self.numImpulses == 1):
            self.totalAmount += 1 # 1 Euro coin
            print("1 Euro")
        elif (self.numImpulses == 2):
            self.totalAmount += 0.5 # 50 Cents coin
            print("50 Cents")

        self.numImpulses = 0

        print(f"Credit: {self.totalAmount}")

        # display.lcd_clear()
        # display.lcd_display_string(f"Credit: {self.totalAmount}", 1)

    def onPulseReceived(self, pin):

        if self.timerObj != None and self.timerObj.is_alive:
                self.timerObj.cancel()

        self.numImpulses += 1
        print('onPulseReceived')
        
        self.timerObj = Timer(
            self.LAST_IMPULSE_TIMEOUT,
            self.registerImpulses)
        
        self.timerObj.start()
          