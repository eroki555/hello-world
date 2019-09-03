"""
Usage example for ADXL355 Python library

This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""

import time
import sys
import numpy as np

t00=time.time()

sys.path.append('/home/pi/.virtualenvs/cv/adxl355-python/lib/')

from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name

t0 = time.time()

print(t0-t00)

x = []
y = []
z = []

t1=time.time()
index=0
while index < 100000:
    axes = device.get_axes() # pylint: disable=invalid-name
    x.append(axes[0])
    y.append(axes[1])
    z.append(axes[2])
    time.sleep(0.00001)
    index += 1

t2=time.time()

print(t2-t1)

