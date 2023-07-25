import board
import neopixel
import time
import threading
import math
import random
import colorsys

# Taken from https://learn.adafruit.com/led-tricks-gamma-correction/the-quick-fix
gammaCorrectedValues_0_255 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36, 37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89, 90, 92, 93, 95, 96, 98, 99, 101, 102, 104, 105, 107, 109, 110, 112, 114, 115, 117, 119, 120, 122, 124, 126, 127, 129, 131, 133, 135, 137, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 167, 169, 171, 173, 175, 177, 180, 182, 184, 186, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213, 215, 218, 220, 223, 225, 228, 231, 233, 236, 239, 241, 244, 247, 249, 252, 255]
gammaCorrectedValues_0_1 = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00392156862745098, 0.00784313725490196, 0.00784313725490196, 0.00784313725490196, 0.00784313725490196, 0.00784313725490196, 0.00784313725490196, 0.00784313725490196, 0.00784313725490196, 0.011764705882352941, 0.011764705882352941, 0.011764705882352941, 0.011764705882352941, 0.011764705882352941, 0.011764705882352941, 0.011764705882352941, 0.01568627450980392, 0.01568627450980392, 0.01568627450980392, 0.01568627450980392, 0.01568627450980392, 0.0196078431372549, 0.0196078431372549, 0.0196078431372549, 0.0196078431372549, 0.023529411764705882, 0.023529411764705882, 0.023529411764705882, 0.023529411764705882, 0.027450980392156862, 0.027450980392156862, 0.027450980392156862, 0.027450980392156862, 0.03137254901960784, 0.03137254901960784, 0.03137254901960784, 0.03529411764705882, 0.03529411764705882, 0.03529411764705882, 0.0392156862745098, 0.0392156862745098, 0.0392156862745098, 0.043137254901960784, 0.043137254901960784, 0.043137254901960784, 0.047058823529411764, 0.047058823529411764, 0.050980392156862744, 0.050980392156862744, 0.050980392156862744, 0.054901960784313725, 0.054901960784313725, 0.058823529411764705, 0.058823529411764705, 0.06274509803921569, 0.06274509803921569, 0.06666666666666667, 0.06666666666666667, 0.07058823529411765, 0.07058823529411765, 0.07450980392156863, 0.07450980392156863, 0.0784313725490196, 0.0784313725490196, 0.08235294117647059, 0.08235294117647059, 0.08627450980392157, 0.08627450980392157, 0.09019607843137255, 0.09411764705882353, 0.09411764705882353, 0.09803921568627451, 0.09803921568627451, 0.10196078431372549, 0.10588235294117647, 0.10588235294117647, 0.10980392156862745, 0.11372549019607843, 0.11372549019607843, 0.11764705882352941, 0.12156862745098039, 0.12549019607843137, 0.12549019607843137, 0.12941176470588237, 0.13333333333333333, 0.13725490196078433, 0.13725490196078433, 0.1411764705882353, 0.1450980392156863, 0.14901960784313725, 0.15294117647058825, 0.15294117647058825, 0.1568627450980392, 0.1607843137254902, 0.16470588235294117, 0.16862745098039217, 0.17254901960784313, 0.17647058823529413, 0.1803921568627451, 0.1843137254901961, 0.18823529411764706, 0.19215686274509805, 0.19607843137254902, 0.19607843137254902, 0.2, 0.20392156862745098, 0.21176470588235294, 0.21568627450980393, 0.2196078431372549, 0.2235294117647059, 0.22745098039215686, 0.23137254901960785, 0.23529411764705882, 0.23921568627450981, 0.24313725490196078, 0.24705882352941178, 0.25098039215686274, 0.25882352941176473, 0.2627450980392157, 0.26666666666666666, 0.27058823529411763, 0.27450980392156865, 0.2823529411764706, 0.28627450980392155, 0.2901960784313726, 0.29411764705882354, 0.30196078431372547, 0.3058823529411765, 0.30980392156862746, 0.3176470588235294, 0.3215686274509804, 0.3254901960784314, 0.3333333333333333, 0.33725490196078434, 0.3411764705882353, 0.34901960784313724, 0.35294117647058826, 0.3607843137254902, 0.36470588235294116, 0.37254901960784315, 0.3764705882352941, 0.3843137254901961, 0.38823529411764707, 0.396078431372549, 0.4, 0.40784313725490196, 0.4117647058823529, 0.4196078431372549, 0.42745098039215684, 0.43137254901960786, 0.4392156862745098, 0.4470588235294118, 0.45098039215686275, 0.4588235294117647, 0.4666666666666667, 0.47058823529411764, 0.47843137254901963, 0.48627450980392156, 0.49411764705882355, 0.4980392156862745, 0.5058823529411764, 0.5137254901960784, 0.5215686274509804, 0.5294117647058824, 0.5372549019607843, 0.5411764705882353, 0.5490196078431373, 0.5568627450980392, 0.5647058823529412, 0.5725490196078431, 0.5803921568627451, 0.5882352941176471, 0.596078431372549, 0.6039215686274509, 0.611764705882353, 0.6196078431372549, 0.6274509803921569, 0.6352941176470588, 0.6431372549019608, 0.6549019607843137, 0.6627450980392157, 0.6705882352941176, 0.6784313725490196, 0.6862745098039216, 0.6941176470588235, 0.7058823529411765, 0.7137254901960784, 0.7215686274509804, 0.7294117647058823, 0.7411764705882353, 0.7490196078431373, 0.7568627450980392, 0.7686274509803922, 0.7764705882352941, 0.7843137254901961, 0.796078431372549, 0.803921568627451, 0.8156862745098039, 0.8235294117647058, 0.8352941176470589, 0.8431372549019608, 0.8549019607843137, 0.8627450980392157, 0.8745098039215686, 0.8823529411764706, 0.8941176470588236, 0.9058823529411765, 0.9137254901960784, 0.9254901960784314, 0.9372549019607843, 0.9450980392156862, 0.9568627450980393, 0.9686274509803922, 0.9764705882352941, 0.9882352941176471, 1 ]

def getMillis():
    ms = time.time_ns() // 1_000_000
    return ms

class ScannerLeds:

    animThread = None
    NUM_PIXELS = 10
    isAnimating = False

    def __init__(self):

        self.pixels = neopixel.NeoPixel(
            board.D10,
            self.NUM_PIXELS,
            brightness=1,
            auto_write=False
            )

        self.pixels.fill((0,0,0))
        self.pixels.show()

    def flickerAnim(self):
        self.pixels.fill((60, 10,0))
        self.pixels.show()

        MIN_INTERVAL = 10
        MAX_ON_INTERVAL_MS = 1000
        MAX_OFF_INTERVAL_MS = 50

        nextChangeTimestamp = getMillis()
        isOn = 1

        while self.isAnimating:
            now = getMillis()

            if now > nextChangeTimestamp:
                if isOn:
                    nextChangeTimestamp = now + random.randint(MIN_INTERVAL,MAX_OFF_INTERVAL_MS)
                    isOn = 0
                else:
                    nextChangeTimestamp = now + random.randint(MIN_INTERVAL,MAX_ON_INTERVAL_MS)
                    isOn = 1

                self.pixels.brightness = isOn
                self.pixels.show()
            

    def scanAnim(self):
        PIXEL_ON_DURATION_MS = 75

        currentPixelOnIndex = 0
        self.pixels[currentPixelOnIndex] = (255,0,0)
        self.pixels.brightness = 1
        self.pixels.show()

        lastPixelChangeTimestamp = getMillis()

        isIncrementing = True

        while self.isAnimating:
            now = getMillis()

            if (now > lastPixelChangeTimestamp + PIXEL_ON_DURATION_MS):
                lastPixelChangeTimestamp = now

                if isIncrementing == True:
                    currentPixelOnIndex += 1
                    self.pixels[currentPixelOnIndex - 1] = (0,0,0)
                    self.pixels[currentPixelOnIndex] = (255,0,0)
                    if currentPixelOnIndex == (self.NUM_PIXELS - 1):
                        isIncrementing = False
                else:
                    currentPixelOnIndex -= 1
                    self.pixels[currentPixelOnIndex + 1] = (0,0,0)
                    self.pixels[currentPixelOnIndex] = (255,0,0)
                    if currentPixelOnIndex == 0:
                        isIncrementing = True

                self.pixels.show()

    def breathAnim(self):
        BREATH_PHASE_MS = 1500
        INCREMENTS_PER_PHASE = 20
        BREATH_INTERVAL_MS = BREATH_PHASE_MS / INCREMENTS_PER_PHASE
        MIN_BRIGHTNESS = 0
        MAX_BRIGHTNESS = 255
        BREATH_INCREMENT = math.floor(MAX_BRIGHTNESS / INCREMENTS_PER_PHASE)

        brightness = 0
        self.pixels.fill((0,255, 0))
        self.pixels.brightness = gammaCorrectedValues_0_1[brightness]
        self.pixels.show()

        lastBrightnessChange = getMillis()
        isIncrementing = True
        
        while self.isAnimating:
            now = getMillis()

            if (now > lastBrightnessChange + BREATH_INTERVAL_MS):
                lastBrightnessChange = now

                if isIncrementing == True:
                    brightness += BREATH_INCREMENT
                    if brightness >= MAX_BRIGHTNESS:
                        brightness = MAX_BRIGHTNESS
                        isIncrementing = False
                else:
                    brightness -= BREATH_INCREMENT
                    if brightness <= MIN_BRIGHTNESS:
                        brightness = MIN_BRIGHTNESS
                        isIncrementing = True

                self.pixels.brightness = gammaCorrectedValues_0_1[brightness]
                self.pixels.show()

    def rainbowAnim(self):
        INTERVAL_MS = 20
        hue = 0
        HUE_INCREMENT = 0.001

        lastChange = getMillis()

        while self.isAnimating:
            now = getMillis()

            if (now > lastChange + INTERVAL_MS):
                lastChange = now

                hue += HUE_INCREMENT

                r,g,b = colorsys.hsv_to_rgb(hue,1,1)
                
                r = math.floor(r * 255)
                g = math.floor(g * 255)
                b = math.floor(b * 255)
                
                self.pixels.fill((r,g,b))
                self.pixels.show()

    def startFlickerAnim(self):
        self.isAnimating = True
        self.animThread = threading.Thread(target=self.flickerAnim)
        self.animThread.start()

    def startScanAnim(self):
        self.isAnimating = True
        self.animThread = threading.Thread(target=self.scanAnim)
        self.animThread.start()

    def startBreathAnim(self):
        self.isAnimating = True
        self.animThread = threading.Thread(target=self.breathAnim)
        self.animThread.start()

    def startRainbowAnim(self):
        self.isAnimating = True
        self.animThread = threading.Thread(target=self.rainbowAnim)
        self.animThread.start()

    def stopAnim(self):
        self.isAnimating = False
        
        if self.animThread != None:
            self.animThread = None

        self.pixels.fill((0,0,0))
        self.pixels.show()