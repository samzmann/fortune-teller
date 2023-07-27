import RPi.GPIO as GPIO
import time

def getMillis():
    ms = time.time_ns() // 1_000_000
    return ms

PIN_TRIGGER = 4
PIN_ECHO = 17

CHECK_INTERVAL_SECONDS = 1
CHECK_INTERVAL_MS = 1000

DISTANCE_CUTOFF_CM = 10 # 10 centimeters

class ProximitySensor:
    isDetecting = False
    lastCheckTimestamp = 0

    def __init__(self, onDetect) -> None:

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        self.onDetect = onDetect

    # def detect(self):
    #     if self.isDetecting == False:
    #         return

    #     now = getMillis()

    #     if self.sentLow == False:
    #         GPIO.output(PIN_TRIGGER, False)
    #         print("Waiting For Sensor To Settle")
    #         self.lastLowTimestamp = now
    #         self.sentLow = True
            
    #     if now > self.lastLowTimestamp + CHECK_INTERVAL_MS:
    #         self.sentLow = False
            
    #         GPIO.output(PIN_TRIGGER, True)
    #         time.sleep(0.00001)
    #         GPIO.output(PIN_TRIGGER, False)

    #         while GPIO.input(PIN_ECHO)==0:
    #             pulse_start = time.time()
            
    #         while GPIO.input(PIN_ECHO)==1:
    #             pulse_end = time.time()
            
    #         pulse_duration = pulse_end - pulse_start
            
    #         distance = pulse_duration * 17150
            
    #         distance = round(distance, 2)

    #         print("Distance: ",distance,"cm")

    #         if distance <= DISTANCE_CUTOFF_CM:
    #             self.isDetecting = False
    #             self.onDetect()
    
    def startDetect(self):
        self.isDetecting = True

    def detect(self):
        if self.isDetecting == False:
            return

        now = getMillis()

        if now > self.lastCheckTimestamp + CHECK_INTERVAL_MS:
            self.lastCheckTimestamp = now

            GPIO.output(PIN_TRIGGER, False)
            print("Waiting For Sensor To Settle")
            time.sleep(CHECK_INTERVAL_SECONDS)
            
            GPIO.output(PIN_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(PIN_TRIGGER, False)
            
            while GPIO.input(PIN_ECHO)==0:
                pulse_start = time.time()
            
            while GPIO.input(PIN_ECHO)==1:
                pulse_end = time.time()
            
            pulse_duration = pulse_end - pulse_start
            
            distance = pulse_duration * 17150
            
            distance = round(distance, 2)

            print("Distance: ",distance,"cm")

            if distance <= DISTANCE_CUTOFF_CM:
                self.isDetecting = False
                self.onDetect()