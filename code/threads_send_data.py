# coding: utf-8


import time
import threading
import serial
import requests

from Read_DHT11 import Dht11

data = {}
lock = threading.RLock()

def get_soil(lock):
    ser = serial.Serial('/dev/rfcomm0', 9600)
    data_soil = ''
    # 读取土壤湿度
    global data
    while True:
        lock.acquire()
        while ser.inWaiting()>0:
            # 读取一行数据
            # max=4090,min=1860,dif=2230,1%=22.3
            data_soil = ser.readline().strip()
            #print data_soil
            soil_1 = str((4090-int(data_soil))/22.3).split('.')
            soil_2 = soil_1[0] + '.' + soil_1[-1][0:2]
            data['soilHum'] = soil_2
        lock.release()

def get_air(lock):
    dh = Dht11(13)

    global data
    while True:
        lock.acquire()
        try:
            air_data = dh.get_data()
            for key in air_data:
                data[key] = air_data[key]
            time.sleep(0.5)
        except:
            print "something error"
            break
        lock.release()

def send_data():
    url = "http://192.168.43.70:8888" + '/bs/setdata/'
    headers = {}

    global data
    while True:
        try:
            time.sleep(2)
            print data
            if data['isRight']:
                response = requests.post(url,data=data,headers=headers)
                print response.json()
            print '-'*50
        except:
            print 'net error'

if __name__ == "__main__":
	soil = threading.Thread(target=get_soil,args=(lock,))
	air = threading.Thread(target=get_air,args=(lock,))
	soil.start()
	air.start()
	time.sleep(6)
	#send = threading.Thread(target=send_data)
	#send.start()
        send_data()
