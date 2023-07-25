import RPi.GPIO as GPIO
import time

def getMillis():
    ms = time.time_ns() // 1_000_000
    return ms

GPIO.setmode(GPIO.BCM)

PIN_EN_A = 18
GPIO.setup(PIN_EN_A, GPIO.OUT)
pi_pwm = GPIO.PWM(PIN_EN_A,1500)
pi_pwm.start(0)
# GPIO.output(PIN_EN_A, True)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

def move():
    print('move')
    GPIO.output(16, True)
    GPIO.output(22, False)

def stop():
    print('stop')
    GPIO.output(16, False)
    GPIO.output(22, False)

isRunning = False

def run():
    global isRunning
    isRunning = True
    lastChange = getMillis()
    isMotorOn = True

    INTERVAL_ON_MS = 5
    INTERVAL_OFF_MS = 50
    
    while isRunning:
        now = getMillis()

        interval = INTERVAL_ON_MS if isMotorOn else INTERVAL_OFF_MS

        if now > lastChange + interval:
            isMotorOn = not isMotorOn
            lastChange = now
            if isMotorOn:
                move()
            else:
                stop()  

def stopRun():
    global isRunning
    isRunning = False