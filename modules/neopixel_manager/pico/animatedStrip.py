import utime
import random
import math

from neopixel import Neopixel
from gammaCorrection import gammaCorrectSingleValue

class AnimatedStrip:

    # 0: off
    # 1: flicker
    # 2: breath green
    # 3: scan
    # 4: rainbow
    animation = 0

    breathBrightness = 0
    hue = 0
    sat = 255
    val = 255

    lastBlinkChange = 0
    isBlinkOn = False

    previousTick = 0

    isBreathIncrementing = True

    scanPixelOnIndex = -1
    isScanIncrementing = True

    def __init__(self, numLeds, stateMachine, pin):
        self.numLeds = numLeds

        self.pixels = Neopixel(
            numLeds,
            stateMachine,
            pin,
            "GRB"
        )

    def resetLeds(self, animType):
        self.pixels.fill((0,0,0))
        
        # Breath green anim should start with brightness 0
        self.pixels.brightness(0 if animType == 2 else 255)
        
        self.lastBlinkChange = utime.ticks_ms()
        self.hue = 0
        self.scanPixelOnIndex = -1
        self.isBreathIncrementing = True
        self.isScanIncrementing = True

    def setAnimation(self, value):
        self.animation = value
        self.resetLeds(value)

    # Resets relevant timestamps if we detect that the value
    # returned by utime.ticks_ms() has wrapped around (eg 1000 -> 0),
    # which is what happens after some time.
    # See docs: https://docs.micropython.org/en/v1.15/library/utime.html#utime.ticks_ms
    def checkTicksWrapAround(self):
        now = utime.ticks_ms()
        if now < self.previousTick:
            self.lastBlinkChange = now
        self.previousTick = now

    def runAnimation(self):
        self.checkTicksWrapAround()

        if self.animation == 0:
            self.animOff()
        elif self.animation == 1:
            self.animFlicker()
        elif self.animation == 2:
            self.animBreathGreen()
        elif self.animation == 3:
            self.animScan()
        elif self.animation == 4:
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

    # Rainbow: animation type 2
    def animBreathGreen(self):
        self.pixels.fill((0,255, 0))

        BREATH_PHASE_MS = 1500
        INCREMENTS_PER_PHASE = 20
        BREATH_INTERVAL_MS = BREATH_PHASE_MS / INCREMENTS_PER_PHASE
        MIN_BRIGHTNESS = 0
        MAX_BRIGHTNESS = 255
        BREATH_INCREMENT = math.floor(MAX_BRIGHTNESS / INCREMENTS_PER_PHASE)

        now = utime.ticks_ms()

        if (now > self.lastBlinkChange + BREATH_INTERVAL_MS):
            self.lastBlinkChange = now

            if self.isBreathIncrementing == True:
                self.breathBrightness += BREATH_INCREMENT
                if self.breathBrightness >= MAX_BRIGHTNESS:
                    self.breathBrightness = MAX_BRIGHTNESS
                    self.isBreathIncrementing = False
            else:
                self.breathBrightness -= BREATH_INCREMENT
                if self.breathBrightness <= MIN_BRIGHTNESS:
                    self.breathBrightness = MIN_BRIGHTNESS
                    self.isBreathIncrementing = True

            self.pixels.brightness(gammaCorrectSingleValue(self.breathBrightness))
            self.pixels.show()

    # Scan: animation type 3
    def animScan(self):
        PIXEL_ON_DURATION_MS = 75
        
        now = utime.ticks_ms()

        if (now > self.lastBlinkChange + PIXEL_ON_DURATION_MS):
            self.lastBlinkChange = now

            if self.isScanIncrementing == True:
                self.scanPixelOnIndex += 1
                self.pixels.set_pixel(self.scanPixelOnIndex - 1, (0,0,0))
                self.pixels.set_pixel(self.scanPixelOnIndex, (255,0,0))
                if self.scanPixelOnIndex == (self.numLeds - 1):
                    self.isScanIncrementing = False
            else:
                self.scanPixelOnIndex -= 1
                self.pixels.set_pixel(self.scanPixelOnIndex + 1, (0,0,0))
                self.pixels.set_pixel(self.scanPixelOnIndex, (255,0,0))
                if self.scanPixelOnIndex == 0:
                    self.isScanIncrementing = True

            self.pixels.show()


    # Rainbow: animation type 4
    def animRainbow(self):
        self.hue += 3
        self.pixels.fill(self.pixels.colorHSV(self.hue, self.sat, self.val))
        self.pixels.show()