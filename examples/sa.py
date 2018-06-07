#!/usr/bin/env python

"""
 @Company
    NVNC Technology, LLC

 @Programmer(s)
    Kenneth A. Jones II
"""

# Copyright (C) NVNC Technology, LLC, 2018 All Rights Reserved. This code may not be copied
# without the express written consent of NVNC Technology, LLC.
#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

import time
import subprocess
from datetime import datetime

if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont

COUNTER = 0
ALM_STATUS = ''

def ip_address():
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    return str(IP.strip())

def show_datetime(draw, device, font):
    dt = datetime.now().strftime('%Y-%m-%d  %I:%M:%S')
    w, h = draw.textsize(dt, font)
    start = (device.width // 2) - (w // 2)
    draw.text((start, 0), dt, font=font, fill="white")

def show_cpu_status(draw, device, font, cpu0, cpu1):
    text = 'CPU0: ACT | CPU1: STBY'
    w, h = draw.textsize(text, font)
    draw.text((0, device.height - h), 'CPU0: ACT | CPU1: STBY', font=font, fill="white")

def show_ip_address(draw, device, message, font):
    w, h = draw.textsize(message, font)
    draw.text((device.width - w, device.height - h), "IP: " + ip_address(), font=font, fill="white")

def update_alarm_info(draw, device, font, msg):
    w, h = draw.textsize(msg, font)
    xstart = (device.width // 2) - (w // 2)
    ystart = (device.height // 2) - (h // 2)
    draw.text((xstart, ystart), msg, font=font, fill="white")

def get_current_alarm():
    import random
    alm_msgs = ['NO ACTIVE ALARMS', 'CHANNEL 1 FAULT', 'CHANNEL 6 OFFLINE', 'CHANNEL 9 ALARM 1', 'CHANNEL 34 ALARM 2',
                'CHANNEL 67 ALARM 3']

    return alm_msgs[random.randint(0, len(alm_msgs) - 1)]

def update(device):
    global ALM_STATUS

    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'pixelmix.ttf')), 16
    font1 = ImageFont.truetype(font_path, size)
    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'pixelmix.ttf')), 8
    font2 = ImageFont.truetype(font_path, size)

    if COUNTER == 0:
        ALM_STATUS = get_current_alarm()

    with canvas(device) as draw:
        show_datetime(draw, device, font2)
        update_alarm_info(draw, device, font1, ALM_STATUS)
        show_cpu_status(draw, device, font2, 0, 0)
        show_ip_address(draw, device, "IP: " + ip_address(), font2)



def main():
    global COUNTER

    sleep_time = 100
    while True:

        update(device)
        if COUNTER == 0:
            COUNTER = 5000
        else:
            COUNTER -= sleep_time

        time.sleep(sleep_time/1000)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
