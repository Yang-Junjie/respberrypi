
# raspberrypi-pico 项目 | 手写体数字识别

我一直有一个想法：在MCU上跑机器学习算法。只不过因为之前的编码能力一直都未能实现，随着自己的编码技术的提升，在周末的空闲时间准备在树莓派pico上跑KNN算法实现手写提数字识别。耗时2天完成了这个项目，其中最大的困难就是pico的RAM空间太小，对数据的处理，使用了卷积+池化的操作对数据进行压缩。

## 材料：

| 名称                   | 数量                          |
| ---------------------- | ----------------------------- |
| 树莓派Pico             | 1个                           |
| 摇杆+按钮/按钮         | 1个5自由度遥感3个按钮/8个按钮 |
| ST7789控制SPI通信LCD屏 | 1个                           |
| 导线                   | 若干                          |

如果有屏幕和按钮合并在一起的模块就不需要上面的按钮、导线、屏幕

![](http://beisent.com/img/raspberrypi/pico/KNN-materials.jpg)

连线参考程序引脚定义，可更改

