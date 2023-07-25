from .Lcd import Lcd

class LcdDisplay:
    line1 = ''
    line2 = ''

    def __init__(self) -> None:
        self.display = Lcd()

    def clear(self):
        self.display.lcd_clear()

    def writeLine1(self, text):   
        self.line1 = text
        self.write()
    
    def writeLine2(self, text):   
        self.line2 = text
        self.write()
    
    def write(self):
        self.clear()
        self.display.lcd_display_string(self.line1, 1)
        self.display.lcd_display_string(self.line2, 2)

dis = LcdDisplay()