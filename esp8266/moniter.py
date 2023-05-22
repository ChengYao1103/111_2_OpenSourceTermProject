# -*- coding: utf-8 -*-
from machine import Pin
from machine import ADC
import time
import network
import dht

def countPercentage(num):
    return round(num*100, 2)

# 設定 ESP8266 連接的 wifi
ssid = ''
password = ''
wifi.active(True)
wifi.connect(ssid, password)

# 連線到 wifi 後再開始設定腳位及偵測
while(not wifi.isconnected()):
    # 每一秒判斷一次是否連上
    time.sleep(1)

# 宣告各感測器的腳位
SOIL_PIN = 0
DHT11_PIN = 0
LDR_PIN = 0

# 設定 ESP8266 板子的 GPIO 腳位
soilPin = Pin(SOIL_PIN, Pin.In)
dhtPin = dht.DHT11(Pin(DHT11_PIN))
ldrPin = ADC(Pin(LDR_PIN))

# 持續執行
while(1):
    # 取得光敏電阻值及計算百分比
    # read_u16 : 0-65535
    lightPercentage = countPercentage(ldrPin.read_u16() / 65535)
    # 觸發偵測溫度與濕度
    dhtPin.measure()
    # 取得溫度與濕度
    humidity = dhtPin.humidity()
    temperature = dhtPin.temperature()
    # 取得連接土壤感測器 pin 腳的的值(0 or 1)
    # 土壤乾燥的話
    if(not soilPin.value()):
        print("土壤乾燥，請澆水")
    else:
        print("土壤濕度足夠")
    # 每 10 秒偵測一次
    time.sleep(10)