#coding: utf-8

import serial

def get_soil_temp():
    ser = serial.Serial('/dev/rfcomm0',9600)
    data = ''

    while 1:
        while ser.inWaiting()>0:
            # 读取一行数据
            data = ser.readline().strip()
            print data

if __name__=="__main__":
    print get_soil_temp()
