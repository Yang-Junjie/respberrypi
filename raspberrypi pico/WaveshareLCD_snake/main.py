from machine import Pin,SPI,PWM
import framebuf
import time
from LCD import LCD_1inch14
import random

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


pwm = PWM(Pin(13))
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
        
        
time.sleep(1)
LCD.fill(0xFFFF)
    
    



