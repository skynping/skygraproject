# coding: utf-8

from Read_soil import *
from Read_DHT11 import Dht11
import requests
import time


def send_data(content, ip):
    url = ip + '/bs/setdata/'
    headers = {}
    response = requests.post(url,data=content,headers=headers)
    return response.json()

while True:
    dh = Dht11(13)
    content = {}
    try:
        content = dh.get_data()
        #content['soilHum'] = read_soil_temp()
        time.sleep(0.5)
        print content
        ip = "http://192.168.43.70:8888"
        res_data = send_data(content, ip)
        print res_data
    except:
        print "something error"
        break
    




