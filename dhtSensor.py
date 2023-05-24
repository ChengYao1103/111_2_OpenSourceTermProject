from machine import Pin
from time import sleep
import dht

# DHT11檢測腳位
DHT_PIN = 14
p14 = Pin(14, Pin.IN)
sensor = dht.DHT11(p14)

i = 0
while True:
    try:
        i += 1
        sleep(2)
        # 測量溫度和濕度
        sensor.measure()
        # 讀取攝氏溫度
        temp = sensor.temperature()
        # 讀取相對溫度
        hum = sensor.humidity()
        # 顯示溫濕度
        print(f"溫度: {temp:3.1f} C")
        print(f"濕度: {hum:3.1f} %")
        # 將數值紀錄到檔案內（buffering 參數為使檔案及時變動，不必等程式結束才看的到資料）
        recordFile = open("./sensorData_dht11.txt", "w", buffering=1, encoding="utf-8")
        recordFile.write(f"第 {i} 次迴圈: 溫度 {temp:3.1f} C, 濕度 {hum:3.1f} %\n")
    except OSError as e:
        print(f"無法讀取感測器: {e}")
    except KeyboardInterrupt:
        print("結束偵測")
        recordFile.close()
