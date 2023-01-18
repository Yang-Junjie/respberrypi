from machine import Pin, I2C, 
from ssd1306 import SSD1306_I2C
from time import sleep
import mpu6050
import math
import time
import math

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height
imu_data = {}


i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400000)
imui2c = I2C(1, scl=Pin(15), sda=Pin(14))

imu = mpu6050.accel(imui2c)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                   

datax = 0
datay = 0
dataz = 0
gAnglex = 0
gAngley = 0
yaw = 0
pitch = 0
roll = 0

def circle(a,b,r):
    x = [i for i in range(-r+a,r+a+1)]
    y = [round(math.sqrt(r**2-(j-a)**2)+b) for j in x]
    not_y = [round(-math.sqrt(r**2-(j-a)**2)+b) for j in x]
    return x,y,not_y

while True:
    imu_data = imu.get_values()
    oled.fill(0)
    # oled.text("X:{}".format(imu_data['GyX']), 0, 0)
    # oled.text("Y:{}".format(imu_data['GyY']), 64, 0)
    # oled.text("Z:{}".format(imu_data['GyZ']), 0, 10)
    # oled.line(0,20, 128, 20,1)
    accx =  (imu_data['AcX'] ) / 131.0
    accy =  (imu_data['AcY'] ) / 131.0
    accz =  (imu_data['AcZ'] ) / 131.0
    
    # print(x, y, z)
    accAnglex = (math.atan(accy /math.sqrt(pow(accx, 2) + pow(accz, 2))) * 180 / math.pi) - 0.58
    accAngleY = (math.atan(-1 * accx / math.sqrt(pow(accy, 2) + pow(accz, 2))) * 180 / math.pi) + 1.58
     
    
    cTime = time.time()
    pTime = cTime
    eTime = (cTime - pTime) / 1000
    
    gyx = imu_data['GyX']   + 0.56
    gyy = imu_data['GyY']   - 2
    gyz = imu_data['GyZ']   + 0.79
    """
    gyx = imu_data['GyX'] / 131.0 + 0.56
    gyy = imu_data['GyY'] / 131.0 - 2
    gyz = imu_data['GyZ'] / 131.0 + 0.79
    """
    gAnglex = gAnglex + gyx * eTime
    gAngleY = gAngley + gyy * eTime
    

    roll = 0.96 * gAnglex + 0.04 * accx
    pitch = 0.96 * gAngley + 0.04 * accy
    
    # print(roll, pitch)
    
    if pitch >=0:
        x = int(64 + pitch * 10)
    else:
        x = int(64 + pitch * 10)
        
    if roll >=0:
        y = int(32 - roll * 10)
    else:
        y = int(32 - roll * 10)
        
    oled.pixel( x, y ,1)
    oled.line(34,32,94,32,1)
    oled.line(64,2,64,62,1)
    
    c_x_1 , c_y_1 , c_not_y_1= circle(64,32,10)
    c_x_2 , c_y_2 , c_not_y_2= circle(64,32,30)
    for i in range(len(c_x_1)):
        oled.pixel(c_x_1[i]-64+x,c_y_1[i]-32+y,1)
        oled.pixel(c_x_1[i]-64+x,c_not_y_1[i]-32+y,1)
    for j in range(len(c_x_2)):
        oled.pixel(c_x_2[j],c_y_2[j],1)
        oled.pixel(c_x_2[j],c_not_y_2[j],1)
        
    """
    oled.text("AcX: {}".format(imu_data['AcX']), 0, 0)
    oled.text("AcY: {}".format(imu_data['AcY']), 15, 20)
    oled.text("AcZ: {})".format(imu_data['AcZ']), 30, 40)
    """
    oled.show()
    sleep(0.001)
    