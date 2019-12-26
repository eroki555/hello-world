"""
Usage example for ADXL355 Python library

This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""

#このプログラムは以下の流れとなっている
#1)loop4_data_get_csv_multi_thread2.pyで作成されたcsvファイルを読み込む
#2)fft処理をする
#3)グラフ化して保存する
#１００回連続でcsvファイルが見つからないときは強制終了する
#現状はこのプログラムを、２つ目のターミナルから実行することでloop4_data_get_csv_multi_thread2.pyと並行処理させる。実行方法は他に方法あるかもしれない。


import time
import sys
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import os



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
