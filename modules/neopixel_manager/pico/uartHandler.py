from machine import Pin,UART

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=1)

def listenUart(onReceiveUartCommand):
    if uart.any():
        received = uart.read(1)
        if received is not None:
            command = int.from_bytes(received, 'little')
            onReceiveUartCommand(command)