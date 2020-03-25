import serial
import time

# m5stack_write = serial.Serial('COM6', 9600, timeout=10)
m5stack = serial.Serial('COM7', 115200, timeout=10)
print('COM7')
# send = b'h'
# send2 = send.encode('utf-8')
# flag=bytes(input(),'utf-8')
# m5stack.write(b'success!!!')
# print('2',send2)
# time.sleep(0.01)
data0 = m5stack.readline()
data0 = data0.decode()
print(data0)
#print(float(data0))
#data1 = data0.strip("\r\n")
#print(data1)
#m5stack.close()
time.sleep(5)


while True:
    #send = b'h'
    #send2 = send.encode('utf-8')
    #flag=bytes(input(),'utf-8')
    #m5stack.write(b'success!!!')
    #print('2',send2)
    #time.sleep(0.01)
    data0 = m5stack.readline()
    data0 = data0.decode()
    #(float(data0))
    data1 = data0.strip("\r\n")
    #print("data1:", data1)
    data2 = data1.split(',')
    print(data2)
    time.sleep(0.1)


m5stack.close()