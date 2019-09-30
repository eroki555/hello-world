"""
Usage example for ADXL355 Python library

This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""

import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime

t00=time.time()

sys.path.append('/home/pi/.virtualenvs/cv/adxl355-python/lib/')

from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name

t0 = time.time()

print(t0-t00)

xg = []
yg = []
zg = []

overrun = 2000
N = 4096
dt=0.00025

device.write_data(0x28, 0x20) #0x00 reset 0x30 HPF 15.545x4 Hz
print('0x28= ',device.read_data(0x28))

#t1=time.time()
index=0
while index < N:
    axes = device.get_axes() # pylint: disable=invalid-name
    xg.append(axes[0])
    yg.append(axes[1])
    zg.append(axes[2])
    time.sleep(0.00001)
    index += 1
#xyz_data = np.array(xyz)

while True:
    axes = device.get_axes()
    if axes[2] < 0.5:
        xg.append(axes[0])
        xg.pop(0)
        yg.append(axes[1])
        yg.pop(0)
        zg.append(axes[2])
        zg.pop(0)
        time.sleep(0.00001)
    elif axes[2] >= 0.5:
        print('Detected!')
        xg.append(axes[0])
        xg.pop(0)
        yg.append(axes[1])
        yg.pop(0)
        zg.append(axes[2])
        zg.pop(0)
        time.sleep(0.00001)
        i = 0
        while i < overrun:
            axes = device.get_axes()
            xg.append(axes[0])
            xg.pop(0)
            yg.append(axes[1])
            yg.pop(0)
            zg.append(axes[2])
            zg.pop(0)
            time.sleep(0.00001)
            i += 1
        #print(zg)
        ZG = zg
        #print(ZG)
        #print(len(ZG))

        #t2=time.time()

        #print(t2-t1)

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
        plt.axis([0, 1/dt/2, -0.1, 0.1])
        
        dt_now = datetime.datetime.now()
        filename = str(dt_now.month) + str(dt_now.day) + str(dt_now.hour) + str(dt_now.minute) + str(dt_now.second) + str(dt_now.microsecond)
        #print(dt_now.month)
        #print(dt_now.month + dt_now.day + dt_now.hour + dt_now.minute + dt_now.second + dt_now.microsecond)
        #print(filename)
        plt.savefig('/home/pi/.virtualenvs/cv/'+filename+'.png')
        print('/home/pi/.virtualenvs/cv/'+filename+'.png', 'saved')
        #acc = np.arange(xg, yg, zg)
        #print(zg)
        with open('/home/pi/.virtualenvs/cv/'+filename+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows([xg, yg, zg])
        print('/home/pi/.virtualenvs/cv/'+filename+'.csv','saved')
        #writer = csv.writer(open('/home/pi/.virtualenvs/cv/'+filename+'.csv', 'ab'))
        #writer.writerow(zg)
        




