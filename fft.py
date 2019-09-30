"""
Usage example for ADXL355 Python library

This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""

import time
import sys
import numpy as np
import matplotlib.pyplot as plt

t00=time.time()

sys.path.append('/home/pi/.virtualenvs/cv/adxl355-python/lib/')

from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name

t0 = time.time()

print(t0-t00)

xg = []
yg = []
zg = []

N = 4096
dt=0.00025

device.write_data(0x28, 0x20) #0x00 reset 0x30 HPF 15.545x4 Hz
print('0x28= ',device.read_data(0x28))

t1=time.time()
index=0
while index < N:
    axes = device.get_axes() # pylint: disable=invalid-name
    xg.append(axes[0])
    yg.append(axes[1])
    zg.append(axes[2])
    time.sleep(0.00001)
    index += 1
t2=time.time()
print(t2-t1)

#print(zg)
ZG = zg
#print(ZG)
print(len(ZG))

t=np.arange(0,N*dt,dt)

F = np.fft.fft(ZG)
F_abs = np.abs(F)
F_abs_amp = F_abs/N*2
F_abs_amp[0]=F_abs_amp[0]/2
fq=np.linspace(0,1.0/dt,N)
fig=plt.figure(figsize=(12,4))

ax2 = fig.add_subplot(121)
plt.xlabel('time(sec)',fontsize=14)
plt.ylabel('amplitude',fontsize=14)
plt.plot(t,ZG)

ax2 = fig.add_subplot(122)
plt.xlabel('freqency(Hz)',fontsize=14)
plt.ylabel('amplitude',fontsize=14)
plt.plot(fq[:int(N)+1],F_abs_amp[:int(N)+1])
plt.axis([0, 1/dt/50, -0.0005, 0.0005])

plt.show()





