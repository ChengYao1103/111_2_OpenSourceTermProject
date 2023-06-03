# -*- coding: utf-8 -*-
from machine import Pin
from machine import ADC
import json
import time
import ntptime
import network
import dht
import urequests

def countPercentage(num):
    return round(num*100, 2)

# 取得設定檔資料
configFile = open("./configs.json", "r")
CONFIGS = json.loads(configFile.read())
configFile.close()

# 設定 ESP8266 連接的 wifi
wifi = network.WLAN(network.STA_IF)
ssid = CONFIGS["wifiSsid"]
password = CONFIGS["wifiPassword"]
wifi.active(True)
wifi.connect(ssid, password)

# 連線到 wifi 後再開始設定腳位及偵測
while(not wifi.isconnected()):
    print("連線中...")
    # 每一秒判斷一次是否連上
    time.sleep(1)
print(wifi.isconnected())

# 透過 ntpServer 更新 esp8266 的時間
ntptime.settime()
# 台灣時間為 UTC+8
TIME_OFFSET = 8 * 60 * 60

# 設定 fireBase realtime database 參數
DATABASE_URL = CONFIGS["realtimeDatabaseUrl"]
DATANODE_NAME = CONFIGS["realtimeDatabaseNode"] + ".json"

# 宣告各感測器的腳位
LDR_PIN = 0     #A0
SOIL_PIN = 16   #D0
DHT11_PIN = 5   #D1

# 設定 ESP12 板子的 GPIO 腳位
soilPin = Pin(SOIL_PIN, Pin.IN)
dhtPin = dht.DHT11(Pin(DHT11_PIN))
ldrPin = ADC(LDR_PIN)

# 初始化要上傳的資料變數
humidity = 0
lightness = 0
temperature = 0
lastWateredTime = time.gmtime(0)

# 持續執行
try:
    while(1):
        # 取得光敏電阻值及計算百分比
        # read_u16 : 0-65535
        lightness = countPercentage(ldrPin.read_u16() / 65535)
        # 觸發偵測溫度與濕度
        dhtPin.measure()
        # 取得溫度與濕度
        humidity = dhtPin.humidity()
        temperature = dhtPin.temperature()
        # 取得當下的時間
        currentTime = time.localtime(time.time() + TIME_OFFSET)
        # 取得連接土壤感測器 pin 腳的的值(0 or 1)
        if(not soilPin.value()):
            hour = currentTime[3]
            # 土壤乾燥且不是中午時段(11~2點)時才澆水
            if(hour < 11 and hour >= 14):
                # 紀錄澆水的時間
                lastWateredTime = currentTime
                print("土壤乾燥，請澆水")
        else:
            print("土壤濕度足夠")

        # data object 儲存 sensor 讀取到的值
        # 格式化(YYYY-MM-DD HH:mm:SS)澆水時間，以字串型態上傳到 firebase
        lastWateredTimeFormat = ""
        for i in range(6):
            # 統一為 2 位數
            if(lastWateredTime[i] < 10):
                lastWateredTimeFormat += "0"
            lastWateredTimeFormat += str(lastWateredTime[i])
            if(i < 2):
                lastWateredTimeFormat += "-"
            elif(i == 2):
                lastWateredTimeFormat += " "
            elif(i < 5):
                lastWateredTimeFormat += ":"
        # data object 儲存 sensor 讀取到的值
        data = {
            "humidity": humidity,
            "lightness": lightness,
            "temperature": temperature,
            "lastWateredTime": lastWateredTimeFormat
        }

        # 將 data object 加入 firebase 中
        response = urequests.post(DATABASE_URL + DATANODE_NAME, json=data)
        if(response.status_code == 200):
            print("ok")
        else:
            print(response.status_code)
        response.close()
        # 每 10 秒偵測一次
        time.sleep(10)

# ctrl C 或是因為其他 error 中斷時
except:
    wifi.disconnect()
    wifi.active(False)
    print("結束偵測")