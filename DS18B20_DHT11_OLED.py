#!/usr/bin/python
import os
import Adafruit_DHT
import math
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from smbus import SMBus

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

font = ImageFont.load_default()
i2cbus = SMBus(1)

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
temp_sensor ='/sys/bus/w1/devices/28-041752f7bbff/w1_slave'


def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c#, temp_f

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

width = disp.width
height = disp.height

disp.clear()
disp.display()

image = Image.new('1', (width, height))

font1 = ImageFont.truetype('FreeSans.ttf', 16)
font2 = ImageFont.truetype('FreeSans.ttf', 16)
font3 = ImageFont.truetype('FreeSans.ttf', 11)

draw = ImageDraw.Draw(image)
x = 0
padding = -2
top = padding
bottom = height-padding

while True:

    temperatura = read_temp()

    humidity, temperature = Adafruit_DHT.read_retry(11, 22)

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    draw.text((x, top), 'DS18B20 + DHT11', font=font3, fill=1)

    draw.text((50, 14), (str(temperatura)[:5]) +' C', font=font2, fill=1)
    draw.text((0, 14), 'Temp', font=font2, fill=1)

    draw.text((x, top+32),    'Humi   {1:0.1f} %'.format(temperature, humidity),         font=font1, fill=1)
    draw.text((x, top+50),    'Temp  {0:0.1f} C'.format(temperature, humidity),    font=font1, fill=1)

    disp.image(image)
    disp.display()
    time.sleep(5)
    print 'DHT11: {0:0.1f} C'.format(temperature, humidity), 'DHT11: {1:0.1f} %'.format(temperature, humidity), 'DS18b20:', (temperatura), 'C'


