from machine import Pin,UART
import time
 
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


while True:
    if uart.any():
        received = uart.read(1)
        if received is not None:
            command = int.from_bytes(received, 'little')
            print("Command received: ", command)
            if command == 1:
                runA()
            if command == 2:
                runB()
            if command == 3:
                runC()

