import machine
import utime

CoinAcceptor = machine.Pin(
    0,
    machine.Pin.IN,
    machine.Pin.PULL_UP,
)

lastImpulseTs = 0

impulseCount = 0
MAX_TICKS_AFTER_LAST_IMPULSE = 1000

MS_AFTER_LAST_IMPULSE = 150

totalAmount = 0

def handleCoinAcceptorImpulse(pin):
    # Disable the interrupt handler while it is running
    CoinAcceptor.irq(handler=None)

    global lastImpulseTs
    global impulseCount

    print('CoinAcceptor.value()', CoinAcceptor.value())

    # For some reason, the interrupt handler is being fired on on rising AND falling edges (despite being configured as machine.Pin.IRQ_FALLING),
    # so here we increment the impulseCount only if CoinAcceptor.value() is 0 (low).
    if CoinAcceptor.value() == 0:
        impulseCount += 1
        lastImpulseTs = utime.ticks_ms()

    # Re-enable the interrupt handler when done
    CoinAcceptor.irq(handler=handleCoinAcceptorImpulse)


CoinAcceptor.irq(
    trigger=machine.Pin.IRQ_FALLING,
    handler=handleCoinAcceptorImpulse
)

def incrementEuros(impulse: int):
    global totalAmount

    if (impulse == 1):
        totalAmount += 1 # 1 Euro coin
        print("1 Euro")
    elif (impulse == 2):
        totalAmount += 0.5 # 50 Cents coin
        print("50 Cents")

def clearImpulseCount():
    global impulseCount
    impulseCount = 0

while True:
    now = utime.ticks_ms()

    if (impulseCount > 0):
        if (now  >= (lastImpulseTs + MS_AFTER_LAST_IMPULSE)):
            print('now  >= (lastImpulseTs + MS_AFTER_LAST_IMPULSE) = ', now  >= lastImpulseTs + MS_AFTER_LAST_IMPULSE)
            print("now:", now)
            print("lastImpulseTs:", lastImpulseTs)
            print("diff:", now - lastImpulseTs)
            incrementEuros(impulseCount)
            clearImpulseCount()

            print("total:", totalAmount)
            print("-- -- --")


