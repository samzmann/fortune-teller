import RPi.GPIO as GPIO
import random

import time

def getMillis():
    ms = time.time_ns() // 1_000_000
    return ms

PIN_IN_A = 16
PIN_IN_B = 20
PIN_EN_A = 18

class BubbleMotor:
    isRunning = False
    isOn = False
    nextChange = 0

    MAX_ON_MS = 2000
    MAX_OFF_MS = 2000
    MIN_INTERVAL_MS = 250

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN_IN_A, GPIO.OUT)
        GPIO.setup(PIN_IN_B, GPIO.OUT)
        GPIO.setup(PIN_EN_A, GPIO.OUT)

        self.pi_pwm = GPIO.PWM(PIN_EN_A,1500)
        self.pi_pwm.start(0)

    def setOn(self):
        GPIO.output(PIN_IN_A, True)
        GPIO.output(PIN_IN_B, False)

    def setOff(self):
        GPIO.output(PIN_IN_A, False)
        GPIO.output(PIN_IN_B, False)

    def runWithIntervals(self):

        if self.isRunning == False:
            return

        now = getMillis()

        if now > self.nextChange:
            if self.isOn:
                self.isOn = False
                self.nextChange = now + random.randint(self.MIN_INTERVAL_MS, self.MAX_OFF_MS)
                self.setOff()
            else:
                self.isOn = True
                self.nextChange = now + random.randint(self.MIN_INTERVAL_MS, self.MAX_ON_MS)
                self.setOn()

    def runSporadic(self):
        self.MAX_ON_MS = 2000
        self.MAX_OFF_MS = 2000
        self.MIN_INTERVAL_MS = 250

        self.isRunning = True
        self.pi_pwm.ChangeDutyCycle(40)
        self.setOn()

    def runVerySporadic(self):
        self.MAX_ON_MS = 2000
        self.MAX_OFF_MS = 5000
        self.MIN_INTERVAL_MS = 250
        
        self.isRunning = True
        self.pi_pwm.ChangeDutyCycle(30)

    def run(self):
        self.runWithIntervals()
    
    def stopRun(self):
        self.isRunning = False