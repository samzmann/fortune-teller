import RPi.GPIO as GPIO
from threading import Timer
from lcd import drivers

GPIO.setmode(GPIO.BCM)
COIN_PIN = 21 # Physical Pin 40
GPIO.setup( COIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

display = drivers.Lcd()
display.lcd_display_string(f"Add coins to", 1)
display.lcd_display_string(f"start", 2)

LAST_IMPULSE_TIMEOUT = 0.150 # 150 ms
numImpulses = 0
totalAmount = 0

timerObj = None

def registerImpulses():
    global numImpulses
    global totalAmount

    if (numImpulses == 1):
        totalAmount += 1 # 1 Euro coin
        print("1 Euro")
    elif (numImpulses == 2):
        totalAmount += 0.5 # 50 Cents coin
        print("50 Cents")

    numImpulses = 0

    display.lcd_clear()
    display.lcd_display_string(f"Credit: {totalAmount}", 1)

def onPulseReceived(pin):
    global numImpulses
    global timerObj

    if timerObj != None and timerObj.is_alive:
            timerObj.cancel()

    numImpulses += 1
    print('onPulseReceived')
    timerObj = Timer(LAST_IMPULSE_TIMEOUT, registerImpulses)
    timerObj.start()


GPIO.add_event_detect(COIN_PIN, GPIO.FALLING)
GPIO.add_event_callback(COIN_PIN, onPulseReceived)
