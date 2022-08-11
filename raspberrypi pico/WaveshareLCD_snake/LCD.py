from machine import Pin,SPI,PWM
import framebuf
import time
import random

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
class Point:#坐标
    row = 0
    col = 0
    def __init__(self,row,col):
        self.row = row
        self.col = col
 
    def copy_self(self):
        return Point(row = self.row,col = self.col)

def rect(Point,colour):#填充坐标
    cell_width = int(W/COL)
    cell_height = int(H/ROW)
    left  = int(Point.col * (W/COL))
    top = int(Point.row * (H/ROW))
    LCD.fill_rect(left,top,cell_width,cell_height,colour)
  
def create_food():#随机生成食物
    while 1:
        pos = Point(random.randint(0,ROW - 1),random.randint(0,COL - 1))
        is_coll = False
        if pos.row == head.row and pos.col == head.col:
            is_coll = True
            break
        for snake in snakes:
            if snake.col == pos.col and snake.row == pos.row:
                is_coll = True
                break
        if not is_coll:
            break
    return pos

if __name__=='__main__':
    while 1 :
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32768)#max 65535
        W = 240
        H = 135
        
        ROW = 15
        COL = 20
        direction = 'left'
        
        LCD = LCD_1inch14()
        LCD.fill_rect(0,0,W,H,LCD.white)
        head = Point(int(ROW/2), int(COL/2))
        head_colour = LCD.red
        
        snake_colour = LCD.blue
        snakes = [
        Point(row = head.row,col = head.col+1),
        Point(row = head.row,col = head.col+2),
        Point(row = head.row,col = head.col+3),
        Point(row = head.row,col = head.col+4),
        ]
        
        food = create_food()
        food_colour = LCD.green
        
        keyA = Pin(15,Pin.IN,Pin.PULL_UP)
        keyB = Pin(17,Pin.IN,Pin.PULL_UP)
        
        key2 = Pin(2 ,Pin.IN,Pin.PULL_UP) #上
        key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)#中
        key4 = Pin(16 ,Pin.IN,Pin.PULL_UP)#左
        key5 = Pin(18 ,Pin.IN,Pin.PULL_UP)#下
        key6 = Pin(20 ,Pin.IN,Pin.PULL_UP)#右
        e = True
        while e :
            if(keyA.value() == 0):
                print("A")
                time.sleep(1)
                continue#按住A键暂停
            if(keyB.value() == 0):
                print("B")
            if(key2.value() == 0):#上
                if direction != 'down':
                        direction = 'up'
                print("UP")
            if(key3.value() == 0):#中
                print("CTRL")
            if(key4.value() == 0):#左
                if direction != 'right':
                        direction = 'left'
                print("LEFT")
            if(key5.value() == 0):#下
                if direction != 'up':
                        direction = 'down'
                print("DOWN")  
            if(key6.value() == 0):#右
                if direction != 'left':
                        direction = 'right'
                print("RIGHT")   
            LCD.show()
            
            #判断是否死亡
            dead = False
            if head.col < 0 or head.row < 0 or head.col >= COL or head.row >= ROW:
                dead = True
            for i in snakes:
                if head.col == i.col and head.row == i.row:
                    dead = True
                    break
            if dead:
                e = False
                LCD.text("game over",85,60,LCD.red)
            
            #判断是否吃到食物
            eat = (head.col == food.col and head.row == food.row)
            snakes.insert(0,head.copy_self())
            if not eat:
                snakes.pop()
            if eat:
                food = create_food()
                
            for i in snakes:
                rect(i, snake_colour)
                
            #移动
            if direction == 'left':
                head.col -= 1
                l = len(snakes)-1
                rect(snakes[l], LCD.white)
            if direction == 'right':
                l = len(snakes)-1
                rect(snakes[l], LCD.white)
                head.col += 1
            if direction == 'up':
                l = len(snakes)-1
                rect(snakes[l], LCD.white)
                head.row -= 1
            if direction == 'down':
                l = len(snakes)-1
                rect(snakes[l], LCD.white)
                head.row += 1
                
            rect(food,food_colour)
            rect(head,head_colour)
            LCD.show()
            
            #游戏重启
        while True:
            if(keyB.value() == 0):
                e = True
                break
        time.sleep(1)
        LCD.fill(0xFFFF)
        
        

