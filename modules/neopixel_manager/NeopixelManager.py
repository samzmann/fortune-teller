import serial
from enum import Enum

class NeopixelCommands(int, Enum):
    SCANNER_OFF = 10
    SCANNER_FLICKER = 11
    SCANNER_BREATH_GREEN = 12
    SCANNER_SCAN = 13
    MOTOR_OFF = 20
    MOTOR_RAINBOW = 24

class NeopixelManager:    
    ser = serial.Serial(
        port='/dev/serial0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        )

    def send(self, cmd: NeopixelCommands):
        print()
        self.ser.write(cmd.to_bytes(1, byteorder='little'))