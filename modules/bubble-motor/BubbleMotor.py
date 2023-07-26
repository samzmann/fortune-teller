import RPi.GPIO as GPIO
from ...modules.utils import getMillis
import random

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
        pi_pwm = GPIO.PWM(PIN_EN_A,1500)
        pi_pwm.start(0)
        pi_pwm.ChangeDutyCycle(30)

    def setOn(self):
        GPIO.output(16, True)
        GPIO.output(22, False)

    def setOff(self):
        GPIO.output(16, False)
        GPIO.output(22, False)

    def runConstant(self):
        print('runConstant')

        isOn = False

        lastChange = getMillis()
        nextChange = lastChange

        MAX_ON_MS = 2000
        MAX_OFF_MS = 2000
        MIN_INTERVAL_MS = 250

        while self.isRunning:
            now = getMillis()

            if now > nextChange:
                if isOn:
                    isOn = False
                    nextChange = now + random.randint(MIN_INTERVAL_MS, MAX_OFF_MS)
                    self.setOff()
                else:
                    isOn = True
                    nextChange = now + random.randint(MIN_INTERVAL_MS, MAX_ON_MS)
                    self.setOn()




    def runSporadic(self):
        print('runConstant')
    
    def stopRun(self):
        self.isRunning = False