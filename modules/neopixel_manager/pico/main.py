from machine import Pin,UART
import time
import utime
import random
from scannerLeds import Strip
from neopixel import Neopixel
from uartHandler import listenUart
 
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=1)

led = Pin(25, Pin.OUT)

def turnOnHalfSec():
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)

def turnOnOneSec():
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)

def runA():
    print('run A')
    turnOnHalfSec()
    
def runB():
    print('run B')
    turnOnHalfSec()
    turnOnHalfSec()

def runC():
    print('run C')
    turnOnHalfSec()
    turnOnHalfSec()
    turnOnHalfSec()

class Strip:
    hue = 0
    sat = 255
    val = 255

    lastBlinkChange = 0
    isBlinkOn = False

    def __init__(self, numLeds, stateMachine, pin):
        self.pixels = Neopixel(
            numLeds,
            stateMachine,
            pin,
            "GRB"
        )

    def hsv(self, h, s, v):
        self.pixels.fill(self.pixels.colorHSV(h, s, v))
        self.pixels.show()
        
    def animRainbow(self):
        self.hue += 3
        self.hsv(self.hue, self.sat, self.val)
    
    def animFlicker(self):

        self.pixels.fill((60, 10,0))
        now = utime.ticks_ms()

        MIN_INTERVAL = 10
        MAX_ON_INTERVAL_MS = 2000
        MAX_OFF_INTERVAL_MS = 50

        if now > self.lastBlinkChange:

            if self.isBlinkOn:
                self.lastBlinkChange = now + random.randint(MIN_INTERVAL,MAX_OFF_INTERVAL_MS)
                self.isBlinkOn = False
                self.pixels.brightness(150)
            else:
                self.lastBlinkChange = now + random.randint(MIN_INTERVAL,MAX_ON_INTERVAL_MS)
                self.isBlinkOn = True
                self.pixels.brightness(20)

            self.pixels.show()


strip = Strip(10, 0, 15)

def onReceiveUartCommand(command):
    print('onReceiveUartCommand', command)

while True:
    listenUart(onReceiveUartCommand)
    strip.animFlicker()


