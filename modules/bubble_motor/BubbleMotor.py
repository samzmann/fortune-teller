import RPi.GPIO as GPIO
import random

import time

def getMillis():
    ms = time.time_ns() // 1_000_000
    return ms

class BubbleMotor:
    isRunning = False

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)

        PIN_IN_A = 16
        PIN_IN_B = 22
        PIN_EN_A = 18

        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(PIN_EN_A, GPIO.OUT)

        self.pi_pwm = GPIO.PWM(PIN_EN_A,1500)
        self.pi_pwm.start(0)

    def setOn(self):
        GPIO.output(16, True)
        GPIO.output(22, False)

    def setOff(self):
        GPIO.output(16, False)
        GPIO.output(22, False)

    def runWithIntervals(self, maxOnMs, maxOffMs, minIntervalMs):
        self.isRunning = True
        self.pi_pwm.ChangeDutyCycle(30)

        isOn = False
        nextChange = getMillis()

        while self.isRunning:
            now = getMillis()


            if now > nextChange:
                if isOn:
                    isOn = False
                    nextChange = now + random.randint(minIntervalMs, maxOffMs)
                    self.setOff()
                else:
                    isOn = True
                    nextChange = now + random.randint(minIntervalMs, maxOnMs)
                    self.setOn()

    def runSporadic(self):
        MAX_ON_MS = 2000
        MAX_OFF_MS = 2000
        MIN_INTERVAL_MS = 250
        self.runWithIntervals(MAX_ON_MS, MAX_OFF_MS, MIN_INTERVAL_MS)


    def runVerySporadic(self):
        MAX_ON_MS = 1000
        MAX_OFF_MS = 10000
        MIN_INTERVAL_MS = 250
        self.runWithIntervals(MAX_ON_MS, MAX_OFF_MS, MIN_INTERVAL_MS)
    
    def stopRun(self):
        self.isRunning = False