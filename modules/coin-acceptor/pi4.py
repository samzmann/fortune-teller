import RPi.GPIO as GPIO
from threading import Timer

LAST_IMPULSE_TIMEOUT = 0.150 # 150 ms
numImpulses = 0
credit = 0

timerObj = None

def registerImpulses():
    global numImpulses
    print(f'registered {numImpulses} impulses')
    numImpulses = 0

def onPulseReceived(pin):
    global numImpulses
    global timerObj

    if timerObj != None and timerObj.is_alive:
            timerObj.cancel()

    numImpulses += 1
    print('onPulseReceived')
    timerObj = Timer(LAST_IMPULSE_TIMEOUT, registerImpulses)
    timerObj.start()

def sT():
    global timerObj
    if timerObj != None and timerObj.is_alive:
            timerObj.cancel()

    timerObj = Timer(LAST_IMPULSE_TIMEOUT, registerImpulses)
    timerObj.start()


GPIO.setmode(GPIO.BCM)
counter_pin = 21 # Physical Pin 40

GPIO.setup( counter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(counter_pin, GPIO.FALLING)
GPIO.add_event_callback(counter_pin, onPulseReceived)
