"""
Usage example for ADXL355 Python library

This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""
#このプログラムは以下の流れとなっている
#1)ADXL355からデータAを取得
#2)データAをcsv化すると同時に、ADXL355からデータBを取得
#3)データBをcsv化すると同時に、ADXL355からデータCを取得
#4)データCをcsv化すると同時に、ADXL355からデータDを取得
#上記を繰り返す

import time
import sys
import numpy as np
import csv
import pandas as pd
#import matplotlib.pyplot as plt
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed

t00=time.time()

#sys.path.append('/home/pi/Documents/')
sys.path.append('/home/pi/hello-world/')


from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name

loop_num = 4096
loop_int = 0.00007 #可変

global index_csv
index_csv = 1

#以下にデータ取得とcsv化のプログラムを２ずつ作っておく

def data_A_get():
	
	t1=time.time()
	xyz = []

	index_data_B=0
	while index_data_B < loop_num:
		axes = device.get_axes() # pylint: disable=invalid-name
		xyz.append(axes)
		time.sleep(loop_int)
		index_data_B += 1

	t2=time.time()

	print('data A get 4000', t2-t1)
	global data_A
	data_A = np.array(xyz)

def data_B_get():
	
	t1=time.time()
	xyz = []

	index_data_B=0
	while index_data_B < loop_num:
		axes = device.get_axes() # pylint: disable=invalid-name
		xyz.append(axes)
		time.sleep(loop_int)
		index_data_B += 1

	t2=time.time()

	print('data B get 4000', t2-t1)
	global data_B
	data_B = np.array(xyz)

def csv_A():
	global index_csv
	index_csv = index_csv
	#csv書き込み時間計測
	t3=time.time()

	header = ['xg','yg','zg']

	with open('/home/pi/adxl355_data/adxl355csv'+str(index_csv)+'.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerows(data_A)
	
	t4=time.time()
	print('write csv A', t4-t3)
	
	index_csv +=1

def csv_B():
	global index_csv
	index_csv = index_csv
	#csv書き込み時間計測
	t3=time.time()

	header = ['xg','yg','zg']

	with open('/home/pi/adxl355_data/adxl355csv'+str(index_csv)+'.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerows(data_B)
	
	t4=time.time()
	print('write csv B', t4-t3)

	index_csv +=1

#まずはdata_A_get()だけ実行しておく
data_A_get()

#ここから並行処理の無限ループに入る
index_loop = 1
#while index_loop < 5:
while True:
	
	t5=time.time()
	executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
	result_B = executor.submit(data_B_get) #data_B_getを実行し、これを変数result_Bとしておく
	executor.submit(csv_A) #csv_Aを実行する(上記と平行)
	as_completed([result_B]).__next__() #data_B_get(result_B)が終了したら、次に進む
	t6=time.time()
	result_A = executor.submit(data_A_get) #data_A_getを実行し、これを変数result_Aとしておく
	executor.submit(csv_B) #csv_Bを実行する(上記と平行)
	as_completed([result_A]).__next__() #data_A_get(result_A)が終了したら、次に進む
	t7=time.time()
	index_loop += 1

print('t6-t5',t6-t5)
print('t7-t6',t7-t6)
print('index_csv',index_csv)


