#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in13
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import socket
import datetime
import os

try:
	epd = epd2in13.EPD()
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)
	
	# Define fonts
	font18 = ImageFont.truetype('fonts/arial.ttf', 18)
	
	# Collect information
	gw = os.popen("ip -4 route show default").read().split()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((gw[2], 0))
	gateway = gw[2]
	host_ip = s.getsockname()[0]
	host_name = socket.gethostname() 

	# Drawing information on diplay
	try:
		image = Image.open('/home/pi/.config/autostart/train.bmp') 
	except:
		image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)  # 255: clear the frame
	draw = ImageDraw.Draw(image)
	draw.text((10, 10), host_name, font = font18, fill = 0)
	draw.text((10, 35), host_ip, font = font18, fill = 0)
	draw.text((10, 65), gateway, font = font18, fill = 0)
	epd.display(epd.getbuffer(image.rotate(180)))
	epd.sleep()
		
except:
	print( 'traceback.format_exc():\n%s',traceback.format_exc())
	exit()