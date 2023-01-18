# raspberrypi-pico 项目 | 水平仪

## 前言

假期闲来无事，在抽屉里找到了之前买来吃灰的mpu6050，这次有时间就随便捣鼓弄出了一个水平仪。在过程中遇到了很多困难，其中最大困难就是对mpu6050的数据进行姿态解算，经过我不断的在网上翻查资料最终就有了以下成就。

![](http://beisent.com/img/raspberrypi/pico/mpu6050.gif)

## 材料

| 材料            | 数量 |
| --------------- | ---- |
| 树莓派 Pico     | 1个  |
| mpu6050         | 1个  |
| oeld096         | 1个  |
| 面包板          | 1个  |
| 杜邦线          | 10根 |
| Micro USB数据线 | 1根  |

## 电路连接

##### 树莓派Pico部分：

树莓派Pico ---> Micro USB ---> 电脑USB![树莓派Pico引脚图](http://beisent.com/img/raspberrypi/pico/pico_pinout.png)

##### MPU6050部分：

| MPU6050 | Raspberry Pi Pico |
| ------- | ----------------- |
| VCC     | VBUS/VSYS/3V3     |
| GND     | GND               |
| SCL     | GP15              |
| SDA     | DP14              |

##### OLED096部分

| OLED096 | Raspberry Pi Pico |
| ------- | ----------------- |
| VCC     | VBUS/VSYS/3V3     |
| GND     | GND               |
| SCL     | GP13              |
| SDA     | GP12              |
