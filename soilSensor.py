import RPi.GPIO as GPIO
import time
# 土壤濕度檢測腳位
SOIL_PIN = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SOIL_PIN, GPIO.IN)

try:
    i = 0
    # 持續偵測
    while(1):
        # 將數值紀錄到檔案內，buffering 參數為使檔案及時變動，不必等程式結束才看的到資料
        recordFile = open("./Desktop/termProject/data.txt", "w", buffering=1, encoding='utf-8')
        recordFile.write(f"第 {i} 次迴圈\n")
        i+=1
        # 土壤乾燥的話
        if(not GPIO.input(SOIL_PIN)):
            print("土壤乾燥，請澆水")
        else:
            print("土壤濕度足夠")
        time.sleep(1)
        # 關閉檔案使檔案內容變動
        recordFile.close()
# ctrl C 中斷時
except KeyboardInterrupt:
    print("結束偵測")
    recordFile.close()
    GPIO.cleanup()