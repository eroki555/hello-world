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

loop_num = 4000
loop_int = 0.000025

x = []
y = []
z = []

t1=time.time()

index=0
while index < loop_num:
    axes = device.get_axes() # pylint: disable=invalid-name
    x.append(axes[0])
    y.append(axes[1])
    z.append(axes[2])
    time.sleep(loop_int)
    index += 1

t2=time.time()
    
x_data = np.array(x)
y_data = np.array(y)
z_data = np.array(z)

print(t2-t1)
#print(x_data)
#print(y_data)
#print(z_data)
#print(x)

x_dup = []
y_dup = []
z_dup = []


#データ重複確認
for i in range(loop_num):
    if x[i-1]==x[i]:
        #print("x data dupulicated!")
        #print(i)
        x_dup.append(i)
        

for i in range(loop_num):
    if y[i-1]==y[i]:
        #print("y data dupulicated!")
        #print(i)
        y_dup.append(i)

for i in range(loop_num):
    if z[i-1]==z[i]:
        #print("z data dupulicated!")
        #print(i)
        z_dup.append(i)
        
print("x_len", len(x_dup))
print("y_len", len(y_dup))
print("z_len", len(z_dup))
