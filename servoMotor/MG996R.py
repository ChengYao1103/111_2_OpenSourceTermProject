'''
參考網站
https://104.es/2021/01/31/%E4%BD%BF%E7%94%A8%E6%A8%B9%E8%8E%93%E6%B4%BE%E9%A9%85%E5%8B%95%E4%BC%BA%E6%9C%8D%E9%A6%AC%E9%81%94sg-90/
https://stackoverflow.com/questions/64621757/mg-996r-servo-raspberry-pi-angle-control
https://p501lab.blogspot.com/2014/07/raspberry-pi-gpio.html
'''
import RPi.GPIO as GPIO
import time

control_pin = 17
pwm_freq = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(control_pin, GPIO.OUT)

#PWM是將類比訊號轉換為脈波的一種技術
#GPIO.PWM(接腳, 頻率)
pwm = GPIO.PWM(control_pin, pwm_freq)
#啟用PWM
pwm.start(0)

#角度轉成工作週期
def angle_to_duty_cycle(angle = 0):
    duty_cycle = (0.05 * pwm_freq) + (0.19 * pwm_freq * angle / 180)
    return duty_cycle

#轉動伺服馬達的角度
def switch_deg(deg):
    dc = angle_to_duty_cycle(deg)
    pwm.ChangeDutyCycle(dc)

degrees = [45, 90, 135, 90]

for i in range(5):
    for deg in degrees:
        switch_deg(deg)
        time.sleep(0.5)

pwm.stop()
GPIO.cleanup()