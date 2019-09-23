import smbus
import time

bus = smbus.SMBus(1)

#放射率設定値 0x24
e = 0.6799

#アドレス
device = 0x5a
device_7bit = 0xb4
emissivity_1 = 0x24
emissivity_2 = 0x2f


def crc8atm(data) :    # data=0x87654321  0b10000111011001010100001100100001 2進数変換
    data =data << 8  # dataを8左シフト    0b1000011101100101010000110010000100000000 (初期値を付加する0x00=00000000,40bit)
    length = len(bin(data)[2:])  # 10000111011001010100001100100001 [2:]...リスト2スライス,0b削除
    for i in range(length):  # lenghtを繰り返す
        if int(bin(data)[2:3], 2) == 1:  # MSB =1,   上位bitが1であるか確かめる
            nokori = bin(data)[11:]  # 11001010100001100100001 [11:]..リスト11スライス
            #  100001110
            #  100000111  XOR:排他的論理和(aまたはbが1の場合bit:1)
            #  000001001  XOR後のDATA
            sentou = (int(bin(data)[2:11], 2)) ^ (int('100000111', 2))  # crc-8=x8+x2+x1+1=100000111
            #  0000010011100101010000110010000100000000  (sentou+nokori)
            #       100000111                            XOR:排他的論理和(aまたはbが1の場合bit:1)
            #       00011111001010000110010000100000000  XOR後のDATA
            data = int((str(bin(sentou)[2:11]) + str(nokori)), 2)
            # dataを2進数から整数にする
            data = int(bin(data), 2)
            # 0111010010
            #  100000111  XOR:排他的論理和(aまたはbが1の場合bit:1)
            #  011010101 <9(9より小さい)
        if len(str(bin(data)[2:])) < 9:
            #  011010101 =0xd5
            return (hex(data))

#温度表示
t1 = bus.read_word_data(0x5a, 0x7)
print(t1)
Tobj1 = t1 * 0.02 - 273.15
print(round(Tobj1,2), 'degC')

#現在の放射率表示 0x04, 0x0f
ems1 = bus.read_word_data(0x5a, 0x24)
print('変更前のems1',ems1)
ems2 = bus.read_word_data(0x5a, 0x2F)
print('変更前のems2', ems2)

#放射率変更
#まず、設定したい放射率は0.6799とする。0x04に入れる値は
e_04 = int(round(65536 * e - 1, 0))
e_04b = bin(e_04)
#e_04hi = int(e_04h)
#print('e_04b', e_04b)
#print(type(e_04b))
e_04bilow = int((e_04b[10:]),2)
#print('e_04bilow', e_04bilow)
#print(hex(e_04bilow))
e_04bihigh = int((e_04b[2:10]),2)
#print('e_04bihigh', e_04bihigh)
#print(hex(e_04bihigh))

#print((0xb424<<16)+(e_04bilow<<8)+(e_04bihigh))
#print(hex((0xb424<<16)+(e_04bilow<<8)+(e_04bihigh)))
#print(type(hex((0xb424<<16)+(e_04bilow<<8)+(e_04bihigh))))

e_04crcdata = int(hex((0xb424<<16)+(e_04bilow<<8)+(e_04bihigh)),16)
#print(e_04crcdata)
#print(hex(e_04crcdata))

    
crc_e_04 = int(crc8atm(e_04crcdata),16)
#print(crc_e_04)
#print(int(crc_e_04, 16))

#0x0fに入れる値を以下の計算式で求める
e_0f = int(round(ems1/e_04*ems2,0))
print('e_0f', hex(e_0f))

#0x0f unlock key  0110 0000
bus.write_word_data(0x5a, 0x60, 0x3c)
####上記PECに入れた値はcrc8atmで0xb460を変換したもの

#以下のData + PECの書き方がわからない
#bus.write_word_data(0x5a, 0x24, [0x00, 0x00, 0x28])
#bus.write_i2c_block_data(0x5a, 0x24, [0xff, 0xff, 0x0c])
#bus.write_word_data(0x5a, 0x24, 0x000028)
#bus.write_word_data(0x5a, 0x24, 0xb4240dae82)
#bus.write_i2c_block_data(0x5a, 0x2f, [0x00, 0x00, 0xc4])
#bus.write_i2c_block_data(0x5a, 0x2f, [0x33, 0x07, 0x17])
#bus.write_word_data(0x5a, 0x2f, 0x0000c4)





#lock = bus.read_word_data(0x5a, 0x60)
#print('lock',lock)


#変更後の放射率表示 0x04, 0x0f
ems12 = bus.read_word_data(0x5a, 0x24)
print('変更後のems1',ems12)
ems22 = bus.read_word_data(0x5a, 0x2F)
print('変更後のems2',ems22)






