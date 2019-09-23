
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

print(crc8atm(0xb42400))
print(crc8atm(0xb42f0000))
