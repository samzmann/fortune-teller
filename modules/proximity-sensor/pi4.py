import RPi.GPIO as GPIO
import time

PIN_TRIGGER = 4
PIN_ECHO = 17

DISTANCE_CUTOFF_CM = 10 # 10 centimeters

class ProximitySensor:

    def __init__(self, onDetect: function) -> None:

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        self.onDetect = onDetect
    
    def startDetect(self):
        
        isDetecting = True

        print("Distance Measurement In Progress")

        CHECK_INTERVAL_SECONDS = 1

        while isDetecting:
                
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

            if distance <= DISTANCE_CUTOFF_CM:
                self.onDetect()
                isDetecting = False

            
            print("Distance: ",distance,"cm")

proximitySensor = ProximitySensor()