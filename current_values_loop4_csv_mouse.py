#!/usr/bin/env

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

t00=time.time()
#print(sys.path)

sys.path.append('/home/pi/Documents/')

#print(sys.path)

#time.sleep(1)

from adxl355 import ADXL355

device = ADXL355()


loop_num = 4096
loop_int = 0.00003 #可変

'''
x = []
y = []
z = []
'''

spi_get_time = []
append_time = []
sleep_time = []
data_4000_get = []
write_csv = []
one_loop_total = []
time_data_total = []

time.sleep(0.1)
print('start')

index=1
r=1
while index <= 50:
	
	t1=time.time()
	
	xyz = []


	index2=0
	while index2 < loop_num:
		ta=time.time()
		axes = device.get_axes() # pylint: disable=invalid-name
		tb=time.time()
		xyz.append(axes)
		tc=time.time()
		time.sleep(loop_int)
		td=time.time()
		index2 += 1

	t2=time.time()
	
	'''
	print('spi get time', tb-ta)
	print('append time', tc-tb)
	print('time sleep', td-tc)
	print('data get 4000', t2-t1)
	'''
	
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
	'''
	print('write csv', t4-t3)
	print('get data and write csv', t4-t1)
	
	spi_get_time.append(tb-ta)
	append_time.append(tc-tb)
	sleep_time.append(td-tc)
	data_4000_get.append(t2-t1)
	write_csv.append(t4-t3)
	one_loop_total.append(t4-t1)
	'''
	time_data =[]
	time_data.append(tb-ta)
	time_data.append(tc-tb)
	time_data.append(td-tc)
	time_data.append(t2-t1)
	time_data.append(t4-t3)
	time_data.append(t4-t1)
	time_data_total.append(time_data)
	
	print(r)
	r +=1
	
data2 = np.array(time_data_total)
#print(xyz)
#print(data)
print(time_data_total)
print(data2)


header2 = ['spi_get_time','append_time','sleep_time','data_4000_get','write_csv','one_loop_total']
with open('/home/pi/adxl355_data/adxl355_time_mouse.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(header2)
	writer.writerows(data2)

	
