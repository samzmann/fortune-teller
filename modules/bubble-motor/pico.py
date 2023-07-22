import machine
import utime

In1 = machine.Pin(6, machine.Pin.OUT)
In2 = machine.Pin(7, machine.Pin.OUT)

# EN_A = machine.Pin(8, machine.Pin.OUT)
# EN_A.high()

EN_A = machine.PWM(machine.Pin(8, machine.Pin.OUT))
EN_A.freq(1500)

def move():
    print('move')
    In1.high()
    In2.low()

def stop():
    print('stop')
    In1.low()
    In2.low()

def dC(num):
    EN_A.duty_u16(int(num))


EN_A.duty_u16(25000)
move()

while True:

    move()

    dC(20000)
    utime.sleep_ms(1000)

    dC(30000)
    utime.sleep_ms(1000)

    dC(000)
    utime.sleep_ms(1000)

    dC(25000)
    utime.sleep_ms(1000)

    stop()
    utime.sleep_ms(1000)