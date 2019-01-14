#!/usr/bin/python
import os
from lib_oled96 import ssd1306
import time

from time import sleep
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from smbus import SMBus

font = ImageFont.load_default()
i2cbus = SMBus(1)
oled = ssd1306(i2cbus)
draw = oled.canvas

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

while True:
    temperature = read_temp()
    draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=20, fill=0)
    font = ImageFont.truetype('FreeSans.ttf', 28)
    draw.text((0, 0), (str(temperature)[:5])+chr(176) +'C', font=font, fill=255)
    oled.display()
    print (temperature)
time.sleep(-time.time() % 1)
