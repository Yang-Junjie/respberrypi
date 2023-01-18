#导入需要用到的库
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import mpu6050
import math
import time

#初始化数据
datax = 0
datay = 0
dataz = 0
gAnglex = 0
gAngley = 0
yaw = 0
pitch = 0
roll = 0
imu_data = {} 
WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height
                                          
 #实例化对象
i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400000)
imui2c = I2C(1, scl=Pin(15), sda=Pin(14))
imu = mpu6050.accel(imui2c)                             
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                   



def circle(a,b,r):
    """画圆函数
    使用圆的标准方程：(x-a)**2+(y-b)**2=r**2
    Args:
        a (int): 圆心的横坐标
        b (int): 圆心的纵坐标
        r (int): 圆的半径

    Returns:
        x (list): 圆上每个点的横坐标
        y (list): 圆上上半圆点的纵坐标
        negative_y (list): 圆上下半圆点的纵坐标
    """
    x = [i for i in range(-r+a,r+a+1)]
    y = [round(math.sqrt(r**2-(j-a)**2)+b) for j in x]
    negative_y = [round(-math.sqrt(r**2-(j-a)**2)+b) for j in x]
    return x,y,negative_y

#主程序
while True:
    imu_data = imu.get_values()#初始化mpu6050基本数据
    oled.fill(0)#清屏

    #对mpu6050数据进行姿态解算
    accx =  (imu_data['AcX'] ) / 131.0
    accy =  (imu_data['AcY'] ) / 131.0
    accz =  (imu_data['AcZ'] ) / 131.0
    
    accAnglex = (math.atan(accy /math.sqrt(pow(accx, 2) + pow(accz, 2))) * 180 / math.pi) - 0.58#x轴角度
    accAngleY = (math.atan(-1 * accx / math.sqrt(pow(accy, 2) + pow(accz, 2))) * 180 / math.pi) + 1.58#y轴角度
     
    cTime = time.time()
    pTime = cTime
    eTime = (cTime - pTime) / 1000
    
    gyx = imu_data['GyX']   + 0.56
    gyy = imu_data['GyY']   - 2
    gyz = imu_data['GyZ']   + 0.79
   
    gAnglex = gAnglex + gyx * eTime
    gAngleY = gAngley + gyy * eTime
    

    roll = 0.96 * gAnglex + 0.04 * accx#翻滚角
    pitch = 0.96 * gAngley + 0.04 * accy#俯仰角
     
    
    if pitch >=0:
        x = int(64 + pitch * 10)#oled屏横坐标
    else:
        x = int(64 + pitch * 10)
        
    if roll >=0:
        y = int(32 - roll * 10)#oled屏纵坐标
    else:
        y = int(32 - roll * 10)
        
    #画基准线
    oled.pixel( x, y ,1)
    oled.line(34,32,94,32,1)
    oled.line(64,2,64,62,1)
    
    #画圆
    c_x_1 , c_y_1 , c_negative_y_1= circle(64,32,10)
    c_x_2 , c_y_2 , c_negative_y_2= circle(64,32,30)
    for i in range(len(c_x_1)):
        oled.pixel(c_x_1[i]-64+x,c_y_1[i]-32+y,1)
        oled.pixel(c_x_1[i]-64+x,c_negative_y_1[i]-32+y,1)
    for j in range(len(c_x_2)):
        oled.pixel(c_x_2[j],c_y_2[j],1)
        oled.pixel(c_x_2[j],c_negative_y_2[j],1)
        

    oled.show()
    time.sleep(0.001)
    
