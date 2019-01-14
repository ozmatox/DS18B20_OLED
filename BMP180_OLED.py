#!/usr/bin/python

import sys
import Adafruit_BMP.BMP085 as BMP085
import os.path
#import Adafruit_DHT
import math
import time
#import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

width = disp.width
height = disp.height

disp.clear()
disp.display()

image = Image.new('1', (width, height))

font1 = ImageFont.truetype('FreeSans.ttf', 18)
font2 = ImageFont.truetype('FreeSans.ttf', 18)
font3 = ImageFont.truetype('FreeSans.ttf', 12)

draw = ImageDraw.Draw(image)
x = 0
padding = -2
top = padding
bottom = height-padding

if len(sys.argv) > 1:
    nbus = sys.argv[1]
elif  os.path.exists("/dev/i2c-0"):
    nbus = "0"
elif os.path.exists("/dev/i2c-1"):
    nbus = "1"
elif os.path.exists("/dev/i2c-2"):
    nbus = "2"
elif os.path.exists("/dev/i2c-3"):
    nbus = "3"

while True:
    sensor = BMP085.BMP085(busnum=int(nbus))

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    draw.text((10, top+0),    'SENSOR BMP180',                                          font=font3, fill=1)
    draw.text((x, top+15),    'Press   ''{0:0.2f}'.format(sensor.read_pressure()*0.01),   font=font1, fill=1)
    draw.text((x, top+31),    'Altitude ''{0:0.2f}'.format(sensor.read_altitude()),     font=font1, fill=1)
    draw.text((x, top+48),    'Temp    ''{0:0.2f}'.format(sensor.read_temperature()),      font=font2, fill=1)


    disp.image(image)
    disp.display()
    time.sleep(.1)


