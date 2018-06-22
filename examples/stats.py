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

#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

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
    return str(IP.strip())

def hostname():
    cmd = "hostname"
    name = subprocess.check_output(cmd, shell=True)
    return str(name.strip())

def cpu_load():
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    return str(CPU.strip())

def mem_usage():
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    return str(MemUsage.strip())

def disk_usage():
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %.1f/%.1fGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    return str(Disk.strip())

def current_time():
    import datetime

    return datetime.datetime.now().strftime('%I:%M %p')

def current_date():
    import datetime

    return datetime.datetime.now().strftime('%Y-%m-%d')

def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

def stats(device):
    # use custom font

    padding = 0
    top = padding
    bottom = device.height - padding
    height_padding = 14

    font_path = None
    size = None

    font_path, size = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'miscfs_.ttf')), 12
    font2 = ImageFont.truetype(font_path, size)



    with canvas(device) as draw:
        top = 0
        draw.text((0, 0), hostname(), font=font2, fill="white")
        draw.text((128, 0), 'Date: ' + current_date(), font=font2, fill="white")
        top += height_padding
        draw.text((0, 14), "IP: " + ip_address(), font=font2, fill="white")
        draw.text((128, 14), 'Time: ' + current_time(), font=font2, fill="white")
        top += height_padding
        draw.text((0, 26), mem_usage(), font=font2, fill="white")
        top += height_padding
        draw.text((0, 38), disk_usage(), font=font2, fill="white")
        #draw.text((0, top), current_time(), font=font2, fill="white")
        draw.text((0, 50), network('wlan0'), font=font2, fill="white")


def main():
    while True:
        stats(device)
        time.sleep(5)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
