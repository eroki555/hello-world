"""
Usage example for ADXL355 Python library
This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""

import time
import sys
import numpy as np
import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import math

sys.path.append('/home/pi/.virtualenvs/cv/adxl355-python/lib')

from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name

device.write_data(0x28, 0x20) #0x00 reset 0x30 HPF 15.545x4 Hz
print('0x28= ',device.read_data(0x28))

offset_x = 0
offset_y = 0
interval = 1
data_len = 10
ave_time = 1000
args = sys.argv
#header = ['cmd','blank','time','XG', 'YG', 'ZG']

#読み込む画像のサイズ自動取得
f = Image.open("/home/pi/Line.png")
print(f.size[0])
print(f.size[1])
W = f.size[0]
H = f.size[1]

def rotate_blit(dst_surf, src_surf, pos, angle, center=True):  
    '''
    画像を回転させてblitする 
    centerがTrueのとき，posはdst_surf上でsrc_surfの中心を差す 
    centerがFalseのとき，posはdst_surf上でsrc_surfの左上を差す 
    '''  
    #回転させたイメージの作成  
    rotateimg = pygame.transform.rotate(src_surf,angle)  
    
    w1, h1 = src_surf.get_size()  #回転前のサイズ  
    w2, h2 = rotateimg.get_size() #回転後のサイズ  
    
    if center:  
        topleft = (pos[0] - w2 / 2, pos[1] - h2 / 2)  
    else:  
        # 回転したことによる中心位置の移動距離  
        dx, dy = (w2 - w1) / 2, (h2 - h1) / 2  
        topleft = (pos[0] - dx, pos[1] - dy)  
        dst_surf.blit(rotateimg, topleft)  
    return rotateimg, topleft  

xyz = []


plt.ion()
fig = plt.figure(figsize=(6,4))
        
#xグラフ
ax1 = fig.add_subplot(211)
ax1.set_ylim(-30,30)
ax1.set_yticks(range(-30,31,10))
ax1.grid(True)
ax1.set_ylabel("x_roll")
        
#yグラフ
ax2 = fig.add_subplot(212, sharex=ax1,sharey=ax1)
ax2.set_ylim(-30,30)
ax2.grid(True)
ax2.set_ylabel("y_pitch")
        
timestp = [float(0.0)] #int(args[4])*int(args[5])/1000
timeud = float(0.0)
x = [float(0.0)]
y = [float(0.0)]

line_x_roll, = ax1.plot(timestp, x, lw=2)
line_y_pitch, = ax2.plot(timestp, y, lw=2)
        
index = 1
while index <= data_len:

    axes_ave_list_x = []
    axes_ave_list_y = []
    axes_ave_list_z = []
    
    for i in range(ave_time):
        axes = device.get_axes()
        axes_ave_list_x.append(float(axes[0]))
        axes_ave_list_y.append(float(axes[1]))
        axes_ave_list_z.append(float(axes[2]))
        time.sleep(0.0003)
    
    acc_x = sum(axes_ave_list_x) / len(axes_ave_list_x)
    #print('axes_ave_list_x', axes_ave_list_x)
    #print(len(axes_ave_list_x))
    ax = float(acc_x)
    print(ax)
        
    acc_y = sum(axes_ave_list_y) / len(axes_ave_list_y)
    ay = float(acc_y)
    print(ay)

    acc_z = sum(axes_ave_list_z) / len(axes_ave_list_z)
    az = float(acc_z)
    print(az)
    
    try:
        roll_x = float(math.degrees(math.asin(ay))+offset_x)
        roll_y = float(math.degrees(math.asin(ax))+offset_y) #デスクの水平レベルの補正値
    except ValueError:
        pass
    
    print('roll x')
    print(roll_x)
    print('roll y')
    print(roll_y)
             
    angle1 = roll_x
    angle2 = roll_y

    timeud += float(interval)
    timestp.append(timeud) #timestp += int(args[4])*int(args[5])/1000

    print(type(x))
    x.append(angle2)
    y.append(angle1)
    index += 1
    print(index)
            
    time.sleep(interval)
    
pygame.init()  
screen = pygame.display.set_mode((900,750),0,32)  
    
x_roll_img = pygame.image.load("/home/pi/x_roll.png")
y_roll_img = pygame.image.load("/home/pi/y_roll.png")
# 画像の描画座標（これが中心を差すかどうかはcenterフラグによって変わる）  
pos1 = 70, 150  
pos2 = 500, 150  
    
image = pygame.image.load("/home/pi/Line.png")
        
font = pygame.font.Font(None, 45)
        
angle = 0  


while True: 
    axes_ave_list_x = []
    axes_ave_list_y = []
    axes_ave_list_z = []
    
    for i in range(ave_time):
        axes = device.get_axes()
        axes_ave_list_x.append(float(axes[0]))
        axes_ave_list_y.append(float(axes[1]))
        axes_ave_list_z.append(float(axes[2]))
        time.sleep(0.0003)
      
    acc_x = sum(axes_ave_list_x) / len(axes_ave_list_x)
    ax = float(acc_x)
    print(ax)
        
    acc_y = sum(axes_ave_list_y) / len(axes_ave_list_y)
    ay = float(acc_y)
    print(ay)

    acc_z = sum(axes_ave_list_z) / len(axes_ave_list_z)
    az = float(acc_z)
    print(az)
    
    try:
        roll_x = float(math.degrees(math.asin(ay))+offset_x)
        roll_y = float(math.degrees(math.asin(ax))+offset_y) #デスクの水平レベルの補正値
    except ValueError:
        pass
    
    print('roll x')
    print(roll_x)
    print('roll y')
    print(roll_y)
             
    pygame.time.wait(100)  
    angle1 = roll_x
    angle2 = roll_y
      
    screen.fill((0,0,0))
    rotate_blit(screen, image, pos1, angle1, False)  
    rotate_blit(screen, image, pos2, angle2, False)
          
    # 描画位置の確認  
    pygame.draw.circle(screen, (255,0,0), (int(pos1[0]+W/2), int(pos1[1]+H/2)), 1)  #画像の中心(回転軸)に赤点を打つ
    pygame.draw.circle(screen, (255,0,0), (int(pos2[0]+W/2), int(pos2[1]+H/2)), 1)  
    screen.blit(x_roll_img, (450,400))
    screen.blit(y_roll_img, (40,400))
    text1 = font.render("Y_axis_Pitch:"+" "+str(round(angle1,4))+"deg", True, (255,255,255))
    text2 = font.render("X_axis_Roll:"+" "+str(round(angle2,4))+"deg", True, (255,255,255))
    xpm = math.tan(math.radians(angle2))*1000
    ypm = math.tan(math.radians(angle1))*1000
    text3 = font.render(str(round(xpm,2))+" "+"mm/m", True, (255,255,255))
    text4 = font.render(str(round(ypm,2))+" "+"mm/m", True, (255,255,255))
    screen.blit(text1,(60,300))
    screen.blit(text2,(470,300))
    screen.blit(text4,(60,350))
    screen.blit(text3,(470,350))
    pygame.display.update()
    
    

    timeud += float(interval)
    timestp.append(timeud) #timestp += int(args[4])*int(args[5])/1000
    timestp.pop(0)

    print(type(x))
    x.append(angle2)
    x.pop(0)
    y.append(angle1)
    y.pop(0)
    index += 1
    print(index)
            
    time.sleep(interval)

    line_x_roll.set_data(timestp, x)
    line_y_pitch.set_data(timestp, y)
    plt.xlim(timestp[-data_len],timestp[-1])
    plt.draw()
    plt.pause(0.001) #float(args[4])*float(args[5])/1000
            
    for e in pygame.event.get():  
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
            

