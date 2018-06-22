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

import subprocess
import time
from datetime import datetime

if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
from luma.core.legacy import text
from luma.core.legacy.font import proportional, SINCLAIR_FONT, TINY_FONT

try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()

def ip_address():
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    return str(IP)

def cpu_load():
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    return str(CPU)

def mem_usage():
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    return str(MemUsage)

def disk_usage():
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    return str(Disk)

def current_time():
    import datetime

    return datetime.datetime.now().strftime('%I:%M:%S')


def stats(device):
    # use custom font

    padding = 0
    top = padding
    bottom = device.height - padding
    height_padding = 15


    font_path = None
    size = None
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts',
    #                                                'C&C Red Alert [INET].ttf')), 16
    # font_path, size  = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'tiny.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'ProggyTiny.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'creep.bdf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'miscfs_.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'FreePixel.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', '8bit_wonder.ttf')), 14
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Minecraft.ttf')), 16
    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'pixelmix.ttf')), 8
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', '5x7.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'code2000.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', '5x7.bdf')), 7
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Minecraftia-Regular.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'digit.ttf')), 16

    # font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Minecraftia-Regular'))
    # font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'digit.ttf'))
    # font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'freefont','FreeSans.ttf'))

    if font_path is not None or  size is not None:
        # print 'Loading font: {} size:{}'.format(font_path, size)
        font2 = ImageFont.truetype(font_path, size)
    else:
        font2 = proportional(SINCLAIR_FONT)


    with canvas(device) as draw:
        top = 0
        draw.text((0, top), "IP: " + ip_address(), font=font2, fill="white")
        top += height_padding
        draw.text((0, top), cpu_load(), font=font2, fill="white")
        top += height_padding
        draw.text((0, top), mem_usage(), font=font2, fill="white")
        top += height_padding
        draw.text((0, top), disk_usage(), font=font2, fill="white")

def cpu0_status(cpu_stat):
    if cpu_stat == "ACT":
        return 'FLT'
    else:
        return 'ACT'

def cpu_status(cpu0, cpu1):
    return 'CPU0:{} CPU2:ACT'.format(cpu0)

def get_channel(alarm):

    return  'NO ACTIVE'  if alarm == " ALARMS" else 'CHANNEL 1'

def active_alarms(alarm):

    if alarm == " ALARMS":
        return ' ALARM 1'

    elif alarm == " ALARM 1":
        return ' ALARM 2'

    elif alarm == ' ALARM 2':
        return ' ALARM 3'

    elif alarm == ' ALARM 3':
        return ' FAULT'

    elif alarm == ' FAULT':
        return ' OFFLINE'

    elif alarm == ' OFFLINE':
        return ' ALARMS'

    else:
        return ' ALARMS'

def main():
    padding = 0
    top = padding
    bottom = device.height - padding
    height_padding = 16

    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'pixelmix.ttf')), 16
    font2 = ImageFont.truetype(font_path, size)
    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'pixelmix.ttf')), 10
    font1 = ImageFont.truetype(font_path, size)

    status = ''
    active_alm = ''
    channel = ''

    while True:
        status = cpu0_status(status)
        active_alm = active_alarms(active_alm)
        channel = get_channel(active_alm)

        with canvas(device) as draw:
            top = 0
            draw.text((0, 0), ip_address(), font=font1, fill="white")
            draw.text((56, 14), channel, font=font2, fill="white")
            draw.text((56, 30), active_alm, font=font2, fill="white")
            draw.text((0, 48), cpu_status(status,status), font=font1, fill="white")
        time.sleep(5)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
