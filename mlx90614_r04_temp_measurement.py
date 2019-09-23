
import smbus
import time

bus = smbus.SMBus(1)


#現在の放射率表示 0x04, 0x0f
ems1 = bus.read_word_data(0x5a, 0x24)
print('現在の放射率',round((ems1+1)/65536, 3))

while True:
    #温度表示
    t1 = bus.read_word_data(0x5a, 0x7)
    Tobj1 = t1 * 0.02 - 273.15
    print('OBJ温度1', round(Tobj1,2), 'degC')
    time.sleep(1)






