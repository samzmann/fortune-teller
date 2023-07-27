from animatedStrip import AnimatedStrip
from neopixel import Neopixel
from uartHandler import listenUart

scannerStrip = AnimatedStrip(10, 0, 15)
bubbleStrip = AnimatedStrip(10, 1, 14)

def onReceiveUartCommand(command):
    print('onReceiveUartCommand', command)

    # Command list:
    # 10: Scanner off
    # 11: Scanner flicker
    # 12: Scanner Breath green
    # 13: Scanner scan

    # 20: Bubble off
    # 24: Bubble rainbow

    if command == 10:
        scannerStrip.setAnimation(0)
    elif command == 11:
        scannerStrip.setAnimation(1)
    if command == 12:
        scannerStrip.setAnimation(2)
    elif command == 13:
        scannerStrip.setAnimation(3)

    elif command == 20:
        bubbleStrip.setAnimation(0)
    elif command == 24:
        bubbleStrip.setAnimation(4)

while True:
    listenUart(onReceiveUartCommand)
    scannerStrip.runAnimation()
    bubbleStrip.runAnimation()


