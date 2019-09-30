"""
Usage example for ADXL355 Python library

This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""

import time
import sys
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import os
from threading import Thread

t00=time.time()

sys.path.append('/home/pi/Documents/')

from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name


def loop4_csv():
	
	loop_num = 4096
	loop_int = 0.00007 #可変

	'''
	x = []
	y = []
	z = []
	'''

	time.sleep(0.1)
	print('start')

	index=1
	while index <= 50:
		
		t1=time.time()
		
		xyz = []


		index2=0
		while index2 < loop_num:
			axes = device.get_axes() # pylint: disable=invalid-name
			xyz.append(axes)
			time.sleep(loop_int)
			index2 += 1

		t2=time.time()
		 

		print('data get 4000', t2-t1)

		data = np.array(xyz)
		#print(data)

		#csv書き込み時間計測
		t3=time.time()

		header = ['xg','yg','zg']

		with open('/home/pi/adxl355_data/adxl355csv'+str(index)+'.csv', 'w') as f:
			writer = csv.writer(f)
			writer.writerow(header)
			writer.writerows(data)
			
		#t4=time.time()
		
		index += 1
		
		t4=time.time()
		print('write csv', t4-t3)
		print('get data and write csv', t4-t1)
		
	'''
		x = data[:,0]
		y = data[:,1]
		z = data[:,2]


		#print(x)
		#print(y)
		print(len(z))

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
				
		#print("x_len", len(x_dup))
		#print("y_len", len(y_dup))
		#print("z_len", len(z_dup))
	'''

def loop_plot():
	
	N = 4096
	dt=0.00025


	index=1
	index_stop=1
	while True:
		t1=time.time()
		
		if os.path.exists('/home/pi/adxl355_data/adxl355csv'+str(index+1)+'.csv') == True:
			index_stop=1
			df = pd.read_csv('/home/pi/adxl355_data/adxl355csv'+str(index)+'.csv', sep=',')

			#print(df['zg'])

			ZG = df['zg']


			#print(len(ZG))

			t=np.arange(0,N*dt,dt)

			F = np.fft.fft(ZG)
			F_abs = np.abs(F)
			F_abs_amp = F_abs/N*2
			F_abs_amp[0]=F_abs_amp[0]/2
			fq=np.linspace(0,1.0/dt,N)
			fig=plt.figure(figsize=(12,4))

			ax1 = fig.add_subplot(121)
			plt.xlabel('time(sec)',fontsize=14)
			plt.ylabel('amplitude',fontsize=14)
			plt.plot(t,ZG)
			plt.axis([0, 1.2, -1.5, 0.5])

			ax2 = fig.add_subplot(122)
			plt.xlabel('freqency(Hz)',fontsize=14)
			plt.ylabel('amplitude',fontsize=14)
			plt.plot(fq[:int(N)+1],F_abs_amp[:int(N)+1])
			plt.axis([0, 1/dt/2, -0.1, 0.1])
			
			plt.savefig('/home/pi/adxl355_data/adxl355'+str(index)+'.png')
			plt.close()


			index +=1
			
		else:
			index_stop += 1
			if index_stop >= 100:
				print('no csv file named',' /home/pi/Documents/adxl355csv',index,'.csv')
				break

		t2=time.time()
		print(round((t2-t1),8))
		
		time.sleep(0.1)

thread_1 = Thread(target=loop4_csv)
thread_2 = Thread(target=loop_plot)


thread_2.start()
thread_1.start()


