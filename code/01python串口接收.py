#coding: utf-8

import serial

ser = serial.Serial('/dev/rfcomm0',9600)
data = ''

while 1:
    while ser.inWaiting()>0:
        # 读取一行数据
        data = ser.readline()
        print data
    #if data != '':
    #    print data
     #   data = ''
