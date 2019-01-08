#coding: utf-8
import RPi.GPIO as GPIO
import time


class Dht11:
    def __init__(self, channel):
        self.channel = channel
    
    def get_data(self):
        #　存放读取的数据
        data = []
        # 设置ｇｐｉｏ管脚模式
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        time.sleep(1)
        
        # 设置成输出模式
        GPIO.setup(self.channel, GPIO.OUT)
        # 主机发送开始信号
        GPIO.output(self.channel, GPIO.LOW)
        #　主机至少拉低１８ｍｓ
        time.sleep(0.02)
        #　主机拉高，开始信号结束
        GPIO.output(self.channel, GPIO.HIGH)
        
        # 设置成输入模式　
        GPIO.setup(self.channel, GPIO.IN)
        # 接收从机低电平响应信号，等待被拉高
        while GPIO.input(self.channel) == GPIO.LOW:
            continue
        # 等待被拉低，开始发送数据
        while GPIO.input(self.channel) == GPIO.HIGH:
            continue
        
        # 开始接收数据
        # 获取４０位数据
        for bit in range(40):
            while GPIO.input(self.channel) == GPIO.LOW:
                continue
            k = 0
            while GPIO.input(self.channel) == GPIO.HIGH:
                k += 1
                if k > 100:
                    break

            if k < 8:
                data.append(0)
            else:
                data.append(1)
        
        GPIO.cleanup()
        
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0

        for i in range(8):
            # 计算湿度
            humidity += data[i] * 2 ** (7 - i)
            humidity_point += data[8 + i] * 2 ** (7 - i)
            # 计算温度
            temperature += data[16 + i] * 2 ** (7 - i)
            temperature_point += data[24 + i] * 2 ** (7 - i)
            # 计算校验值
            check += data[32 + i] * 2 ** (7 - i)

        isRight = check == humidity + humidity_point + temperature + temperature_point
        temp =  str(temperature) + "." + str(temperature_point)
        hum = str(humidity) + "." + str(humidity_point)
        
        return {"isRight":isRight,"temp": temp, "hum": hum}

def main():
    dh = Dht11(13)
    wrong_count = 0
    for i in range(100):
        print "hello"
        content = dh.get_data()
        print  content["isRight"]
        print "temp:" + content["temp"] + ", "  + "hum: " + content["hum"]
        time.sleep(2)

        if content['isRight'] == False:
            wrong_count+=1

    print wrong_count
    

if __name__ == "__main__":
    main()

