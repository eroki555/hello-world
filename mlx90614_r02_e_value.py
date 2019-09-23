#このプログラムは、設定したい放射率εを入力し実行すると、EEPROMの0x04(0x24)と0x0f(0x2f)の値が自動で書き換わる。


import smbus
import time

bus = smbus.SMBus(1)

#放射率設定値 0x24
e = 1 #                                       ←←←　ここにεを入力
print('設定したい放射率e', e)

#アドレス
device = 0x5a
device_7bit = 0xb4
ems1_ad = 0x24
ems2_ad = 0x2f


#現在の放射率表示 0x04, 0x0f
ems1 = bus.read_word_data(0x5a, 0x24)
print('変更前のems1',ems1)
ems2 = bus.read_word_data(0x5a, 0x2F)
print('変更前のems2', ems2)


#温度表示
t1 = bus.read_word_data(0x5a, 0x7)
#print(t1)
Tobj1 = t1 * 0.02 - 273.15
print('ems変更前の温度', round(Tobj1,2), 'degC')



#変更したい数値
ems1_val = int(round(65536 * e - 1, 0))
print('設定したいems1', ems1_val)
ems2_val = int(round(ems1/ems1_val*ems2,0))
print('設定したいems2', ems2_val)



def crc8atm(data) :    # data=0x87654321  0b10000111011001010100001100100001 2進数変換
    data =data << 8  # dataを8左シフト    0b1000011101100101010000110010000100000000 (初期値を付加する0x00=00000000,40bit)
    length = len(bin(data)[2:])  # 10000111011001010100001100100001 [2:]...リスト2スライス,0b削除
    for i in range(length):  # lenghtを繰り返す
        if int(bin(data)[2:3], 2) == 1:  # MSB =1,   上位bitが1であるか確かめる
            nokori = bin(data)[11:]  # 11001010100001100100001 [11:]..リスト11スライス

            sentou = (int(bin(data)[2:11], 2)) ^ (int('100000111', 2))  # crc-8=x8+x2+x1+1=100000111

            data = int((str(bin(sentou)[2:11]) + str(nokori)), 2)
            
            data = int(bin(data), 2)

        if len(str(bin(data)[2:])) < 9:
            
            return (hex(data))


#ems1_valに対するcrc値取得 crc_ems1

if ems1_val > 255:
    ems1_low = bin(ems1_val)[-8:]
    ems1_high = bin(ems1_val)[2:len(bin(ems1_val))-len(ems1_low)]
    ems1_low =int((ems1_low),2)
    ems1_high = int((ems1_high),2)


else:
    ems1_low = int(bin(ems1_val)[2:],2)
    ems1_high = 0

print('ems1_low', hex(ems1_low))
print('ems1_high', hex(ems1_high))

#crc_ems1
crc_ems1 = (0xb424<<16)+(ems1_low<<8)+ems1_high
#print(type(crc_ems1))
#print(hex(crc_ems1))
#print(bin(crc_ems1))

crc_ems1 = int(crc8atm(crc_ems1),16)
print(crc_ems1, hex(crc_ems1))


#ems2_valに対するcrc値取得 crc_ems2

if ems2_val > 255:
    ems2_low = bin(ems2_val)[-8:]
    ems2_high = bin(ems2_val)[2:len(bin(ems2_val))-len(ems2_low)]
    ems2_low =int((ems2_low),2)
    ems2_high = int((ems2_high),2)


else:
    ems2_low = int(bin(ems2_val)[-8:],2)
    ems2_high = 0

print('ems2_low',hex(ems2_low))
print('ems2_high',hex(ems2_high))

#crc_ems1
crc_ems2 = (0xb42f<<16)+(ems2_low<<8)+ems2_high
#print(type(crc_ems2))
#print(hex(crc_ems2))
#print(bin(crc_ems2))

crc_ems2 = int(crc8atm(crc_ems2),16)
print(crc_ems2,hex(crc_ems2))

#0x0f unlock key  0110 0000
bus.write_word_data(0x5a, 0x60, 0x3c)

#ems1変更
bus.write_i2c_block_data(0x5a, 0x24, [0x00, 0x00, 0x28]) #0入力
time.sleep(1)
bus.write_i2c_block_data(0x5a, 0x24, [ems1_low, ems1_high, crc_ems1]) #希望の値入力
#bus.write_i2c_block_data(0x5a, 0x24, [0xff, 0xff, 0x0c]) #希望の値入力
time.sleep(1)


#ems2変更
bus.write_i2c_block_data(0x5a, 0x2f, [0x00, 0x00, 0xc4])
time.sleep(1)
bus.write_i2c_block_data(0x5a, 0x2f, [ems2_low, ems2_high, crc_ems2])
time.sleep(1)






#lock = bus.read_word_data(0x5a, 0x60)
#print('lock',lock)


#変更後の放射率表示 0x04, 0x0f
ems12 = bus.read_word_data(0x5a, 0x24)
print('変更後のems1',ems12)
ems22 = bus.read_word_data(0x5a, 0x2F)
print('変更後のems2',ems22)

#温度表示
t2 = bus.read_word_data(0x5a, 0x7)
#print(t1)
Tobj2 = t2 * 0.02 - 273.15
print('ems変更後の温度', round(Tobj2,2), 'degC')





