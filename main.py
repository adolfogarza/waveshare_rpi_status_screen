#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in13
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd2in13.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # # partial update
    print("Show time")
    epd.init(epd.PART_UPDATE)    
    epd.Clear(0xFF)
    font15 = ImageFont.truetype('fonts/arial.ttf', 15)
    time_image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255) # 255: clear the frame
    time_draw = ImageDraw.Draw(time_image)
    while (True):
        time_draw.rectangle((10, 10, 120, 50), fill = 255)
        time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font15, fill = 0)
        newimage = time_image.crop([10, 10, 120, 50])
        time_image.paste(newimage, (10,10))  
        epd.displayPartial(epd.getbuffer(time_image))
        
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()

