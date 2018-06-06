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
    # font_path, size  = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'tiny.ttf')), 12
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'ProggyTiny.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'creep.bdf')), 16
    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'miscfs_.ttf')), 12
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'FreePixel.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', '8bit_wonder.ttf')), 14
    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Minecraft.ttf')), 8
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'pixelmix.ttf')), 12
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', '5x7.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'code2000.ttf')), 16
    # font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', '5x7.bdf')), 7
    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Minecraftia-Regular.ttf')), 8
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
        # draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        # if device.height >= 32:
        #     draw.text((0, 14), mem_usage(), font=font2, fill="white")
        #
        # if device.height >= 64:
        #     draw.text((0, 26), disk_usage('/'), font=font2, fill="white")
        #     try:
        #         draw.text((0, 38), network('wlan0'), font=font2, fill="white")
        #     except KeyError:
        #         # no wifi enabled/available
        #         pass

        top = 0
        draw.text((0, top), "IP: " + ip_address(), font=font2, fill="white")
        top += height_padding
        draw.text((0, top), cpu_load(), font=font2, fill="white")
        top += height_padding
        draw.text((0, top), mem_usage(), font=font2, fill="white")
        top += height_padding
        # draw.text((0, top), disk_usage(), font=font2, fill="white")
        draw.text((0, top), current_time(), font=font2, fill="white")


def main():
    while True:
        stats(device)
        time.sleep(.5)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
