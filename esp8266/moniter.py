# -*- coding: utf-8 -*-
from machine import Pin
from machine import ADC
import time
import network
import dht

def countPercentage(num):
    return round(num*100, 2)

# 設定 ESP8266 連接的 wifi
wifi = network.WLAN(network.STA_IF)
ssid = ''
password = ''
wifi.active(True)
wifi.connect(ssid, password)

# 連線到 wifi 後再開始設定腳位及偵測
while(not wifi.isconnected()):
    print("連線中...")
    # 每一秒判斷一次是否連上
    time.sleep(1)
    
print(wifi.isconnected())

# 宣告各感測器的腳位
LDR_PIN = 0     #A0
SOIL_PIN = 16   #D0
DHT11_PIN = 5   #D1

# 設定 ESP12 板子的 GPIO 腳位
soilPin = Pin(SOIL_PIN, Pin.IN)
dhtPin = dht.DHT11(Pin(DHT11_PIN))
ldrPin = ADC(LDR_PIN)

# 持續執行
try:
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
        if(not soilPin.value()):
            # 土壤乾燥的話
            print("土壤乾燥，請澆水")
        else:
            print("土壤濕度足夠")
        # 每 10 秒偵測一次
        time.sleep(10)
# ctrl C 中斷時
except KeyboardInterrupt:
    wifi.disconnect()
    wifi.active(False)
    print("結束偵測")