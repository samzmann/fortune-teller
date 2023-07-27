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

    # 0: off
    # 1: flicker
    # 2: breath green
    # 3: scan
    # 4: rainbow
    animation = 0

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

    def resetLeds(self):
        self.pixels.fill((0,0,0))
        self.pixels.brightness(255)
        self.lastBlinkChange = utime.ticks_ms()
        self.hue = 0

    def setAnimation(self, value):
        self.animation = value
        self.resetLeds()

    def runAnimation(self):
        if self.animation == 0:
            # print('off')
            self.animOff()
        elif self.animation == 1:
            # print('animFlicker')
            self.animFlicker()
        elif self.animation == 2:
            print('animBreathGreen')
            # self.animBreathGreen()
        elif self.animation == 3:
            print('animScan')
            # self.animScan()
        elif self.animation == 4:
            # print('animRainbow')
            self.animRainbow()
    
    # Off: animation type 0
    def animOff(self):
        self.pixels.fill((0,0,0))
        self.pixels.show()
    
    # Flicker: animation type 1
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

    # Rainbow: animation type 4
    def animRainbow(self):
        self.hue += 3
        self.pixels.fill(self.pixels.colorHSV(self.hue, self.sat, self.val))
        self.pixels.show()

scannerStrip = Strip(10, 0, 15)
bubbleStrip = Strip(10, 1, 14)

def onReceiveUartCommand(command):
    print('onReceiveUartCommand', command)

    # Command list:
    # 10: Scanner off
    # 11: Scanner flicker
    # 12: Scanner Breath green
    # 13: Scanner scan

    # 20: Bubble off
    # 24: Bubble rainbow

    if command == 10:
        scannerStrip.setAnimation(0)
    elif command == 11:
        scannerStrip.setAnimation(1)
    if command == 12:
        scannerStrip.setAnimation(2)
    elif command == 13:
        scannerStrip.setAnimation(3)

    elif command == 20:
        bubbleStrip.setAnimation(0)
    elif command == 24:
        bubbleStrip.setAnimation(4)

while True:
    listenUart(onReceiveUartCommand)
    scannerStrip.runAnimation()
    bubbleStrip.runAnimation()


