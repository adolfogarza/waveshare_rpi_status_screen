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
	# initial display clear
	epd = epd2in13.EPD()
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)
	
	# font
	preferredFont = ImageFont.load_default()
	
	# variables
	current_ssid = ""
	current_host_name = ""
	current_host_ip = ""
	current_gateway = ""
	
	while True:
		# get most updated internet data values
		gw = os.popen("ip -4 route show default").read().split()
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect((gw[2], 0))
		gateway = gw[2]
		host_ip = s.getsockname()[0]
		host_name = socket.gethostname()
		ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()

		if current_ssid != ssid or current_host_name != host_name or current_host_ip != host_ip or current_gateway != gateway:
			current_ssid = ssid
			current_host_name = host_name
			current_host_ip = host_ip
			current_gateway = gateway

			# draw on display
			image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)  # 255: clear the frame
			draw = ImageDraw.Draw(image)
			draw.text((10, 10), f'ssid: {current_ssid}', font = preferredFont, fill = 0)
			draw.text((10, 25), f'host name: {current_host_name}', font = preferredFont, fill = 0)
			draw.text((10, 40), f'host ip: {current_host_ip}', font = preferredFont, fill = 0)
			draw.text((10, 55), f'gateway: {current_gateway}', font = preferredFont, fill = 0)
			epd.display(epd.getbuffer(image.rotate(180)))
			epd.sleep()
		
		time.sleep(10)
		
except:
	print( 'traceback.format_exc():\n%s',traceback.format_exc())
	exit()