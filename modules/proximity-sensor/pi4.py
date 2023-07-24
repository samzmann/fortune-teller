import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

PIN_TRIGGER = 4
PIN_ECHO = 17

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

print("Distance Measurement In Progress")

CHECK_INTERVAL_SECONDS = 1

try:
    while True:
        
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
        
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
    print("Cleaning up!")
    GPIO.cleanup()