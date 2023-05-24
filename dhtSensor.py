from machine import Pin
from time import sleep
import dht

sensor = dht.DHT22(Pin(14))
# sensor = dht.DHT11(Pin(14))

while True:
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("溫度: %3.1f C" % temp)
        print("濕度: %3.1f %%" % hum)
    except OSError as e:
        print("Failed to read sensor.")
