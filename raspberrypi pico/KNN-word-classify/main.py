from LCD import LCD_1inch3
from machine import Pin,PWM
import json,time,os,math



gird_size = 16
trian_data_address = r'data/trian_data/'#训练集文件目录
target_data_address = r'data/target/'#存放目标文件目录

trian_file =  (os.listdir(trian_data_address))#获得训练集文件夹下所有文件
target_file = (os.listdir(target_data_address))#获得目标文件夹下所有文件
 
trian_length = len(trian_file)#训练集文件夹中的文件数
target_length = len(target_file)#目标文件夹中的文件数

def boradcast_sqrt(bslist):
    """
    输入：列表
    输出：对列表中每个数进行算术平方根后给出一个新列表
    """
    return [i**0.5 for i in bslist]

def broadcast_power(bslist,num):
    """
    输入：列表
    输出：对列表中每个数字进行num的幂运算给出一个运算完后的列表
    """
    return [i**num for i in bslist]
    
def list_sum(bslist):
    """
    输入:列表
    输出：对列表中所有的数进行求和给出求和后的结果
    """
    a = 0
    for i in bslist:
        a += i
    return a

def bslist_opertion_subtraction(lista,listb):
    """
    输入：列表a，列表b
    输出：对列表索引相对应的数进行减法运算，给出运算完后的列表
    列表a-列表b
    """
    return [lista[i]-listb[i] for i in range(len(lista))]
  
def get_data(address,file,length):
    """
    输入：地址，文件名，地址中文件的数量
    输出：对应地址文件的所有数据列表[{'key':'文件名的第一个字符','value':'[手写数据]'}....,{}]
    """
    data_set=[]
    for z in range(length):
        b=[]
        data={'key' : None,'value' :None }
        file_name =file[z]
        data['key'] = file_name[:1]
        with open(address+f'{file_name}','r+') as f:
            a = json.load(f)
        for i in a:
            for j in i:
                b.append(j)
        data['value'] = b
        data_set.append(data)
    return data_set

def dic_separate(data_set):
    """
    输入：函数get_data的返回值
    输出：key，value 一一对应的两个列表
    """
    value_set = []
    keys_set = []
    for i in data_set:
        keys = i['key']
        keys_set.append(keys)
        values = i['value']
        value_set.append(values)
    return value_set,keys_set
    
def distance(trian_data,target,k):
    """
    输入:函数dic_separate返回的value_set
    trian_data为dic_separate返回的训练集value_set
    target为dic_separate返回的目标文件的value_set
    返回：距离，key 一一对应的两个列表
    """
    a = -1
    dis= []
    labels = []
    trian = dic_separate(trian_data)
    for i in trian[0]:
        q = math.sqrt(list_sum(broadcast_power(bslist_opertion_subtraction(target,i),2)))
        a+=1
        label = trian[1][a]
        dis.append(q)
        labels.append(label)
    return dis,labels



def data_sort(data,k):
    """
    输入：函数distance返回的dis
    输出：距离最近的k个数据[{'value':距离 , 'label': '对应的标签'},....., {}]并给出label出现次数最对的label
    """
    final_list = []
    b =[]
    for i in range(len(data[0])):
        a={'value':None,'label':None}
        a['value']=data[0][i]
        a['label']=data[1][i]
        b.append(a)
    m = sorted(b,key=lambda x: x['value'])
    for j in range(k):
        final_list.append(m[j])
    max_count = 0
    max_label = None
    for item in final_list:
        label = item['label']
        count = 0
        for i in final_list:
            if i['label'] == label:
                count += 1
        if count > max_count:
            max_count = count
            max_label = label
    return final_list,max_label

def rect(init_x=None,init_y=None,end_x=None,end_y=None,size=None,fill=None,mid_x=None,mid_y=None,grid=None,grid_num_x=None,grid_num_y=None):
    """
    输入：
    init_x(int) : 矩形左上角的横坐标
    init_y(int) : 矩形左上角的纵坐标
    end_x(int) : 矩形右下角的横坐标
    end_y(int) : 矩形右下角的纵坐标
    size(int)  :矩形的尺寸;如果fill为True则为中心点的偏移量False则为边框的尺寸
    fill(int)  ：矩形是否填充
    mid_x(int) : 只有fill为True才有实际作用，为矩形中心点的横坐标
    mid_y(int) : 只有fill为True才有实际作用，为矩形中心点的纵坐标
    grid(Bool) :True则显示网格
    grid_num_x:竖线条数
    grid_num_y：横线条数
    
    """
    if mid_x != None and mid_y !=None:
        init_x = mid_x - size
        init_y = mid_y - size
        end_x = mid_x + size
        end_y = mid_y + size
    d_x = end_x-init_x
    d_y = end_y-init_y
    move_x=(end_x-init_x)/grid_num_x
    for n in range(size):
        if n == 0:
            if fill == True:
                LCD.fill_rect(init_x,init_y,d_x,d_y,1)                             
            else:
                LCD.rect(init_x,init_y,d_x,d_y,1)
        else:
            change = int(-(((-1)**n)*(1/2)*(n+((1/2)*(1-((-1)**n))))))
            change_x,change_y = init_x+change,init_y+change
            if fill == True:
                LCD.fill_rect(change_x,change_y,end_x-change-change_x,end_y-change-change_y,1)
            else:
                LCD.rect(change_x,change_y,end_x-change-change_x,end_y-change-change_y,1)
                
    if grid == True and grid_num_y != None and grid_num_x != None :
        height = end_y-init_y
        width = end_x-init_x
        w_num = int(width/grid_num_x)
        h_num = int(height/grid_num_y)
        dy = init_y
        dx = init_x
        for h in range(grid_num_y-1):
            dy = dy + h_num
            LCD.line(init_x,dy,end_x,dy,1)
        for w  in range(grid_num_x-1):
            dx = dx + w_num
            LCD.line(dx,init_y,dx,end_y,1)
    return init_x,init_y,end_x,end_y,size,grid_num_x,grid_num_y,move_x



class Pointer:
    def __init__(self,x,y,size):
        self.x = gird_size/2
        self.y = gird_size/2
        self.size = 3
    
        
if __name__=='__main__':
    #初始化
    pwm = PWM(Pin(13))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535
    LCD = LCD_1inch3()
    out = 0
    LCD.fill(LCD.white)
    X = LCD.width
    Y = LCD.height
    draw_board = rect(init_x=3,init_y=3,end_x=Y-3,end_y=Y-3,size=4,fill=False,grid=False,grid_num_y=gird_size,grid_num_x=gird_size)
    pointer = Pointer(int(draw_board[0]+draw_board[2]/2),int(draw_board[1]+draw_board[1]/2),2) 
    LCD.show()
    
    
    
    def zhuangbi():
        global pointer,out,X,Y
        for x in range(Y,X):
            y =  int((30 +math.sin(3.14/30*x+pointer.x)*(20-out))/X*Y)
            y1 = int((30 +math.cos(3.14/40*x+pointer.y)*(20-out))/X*Y)
            LCD.pixel(x,y,LCD.Orange)
            LCD.pixel(x,y1,LCD.green)
        
            
    data = [ [0] * gird_size for i in range(gird_size)]#初始化data
    
    count = 0#用于计数
    
    #实例化Pin对象
    keyA = Pin(15,Pin.IN,Pin.PULL_UP)#A
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)#B
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP) #上
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)#中
    key4 = Pin(16 ,Pin.IN,Pin.PULL_UP)#左
    key5 = Pin(18 ,Pin.IN,Pin.PULL_UP)#下
    key6 = Pin(20 ,Pin.IN,Pin.PULL_UP)#右
    model = 0 #0是移动笔，1是画
    result_list = None
    result = None
    while(1):
        if Y%15 != 0 or Y<90 or Y>135:
            print("Y的值不被允许")
            break
        move_distance = int(draw_board[7])
        #print(move_distance)
        
        if model == 0:
            LCD.fill(LCD.white)
            zhuangbi()
        if model == 1:
            data[int(pointer.y/move_distance)-1][int(pointer.x/move_distance)-1] = 1
        
        #文本信息
        LCD.text(f'This letter',Y,Y-35,1)
        LCD.text(f'is',Y,Y-25,1)
        LCD.text(f'{result}',Y+20,Y-25,LCD.red)
        LCD.text("BS-KNN-ES",Y,Y-50,LCD.blue)
        LCD.text("Beisent.com",Y,Y-15,LCD.blue)
        
        draw_board = rect(init_x=3,init_y=3,end_x=Y-3,end_y=Y-3,size=4,fill=False,grid=False,grid_num_y=gird_size,grid_num_x=gird_size)
        draw_pen = rect(mid_x=int(pointer.x),mid_y =int( pointer.y), size=pointer.size,fill=True,grid_num_y=gird_size,grid_num_x=gird_size)
        LCD.show()
       
        if out == 20:
            break
        #print(out)
        if(keyA.value() == 0):
            model =1
            out = 0
        if(keyB.value() == 0):
            model = 0
            out = 0
            count+=1
            
#             with open(f'data/trian_data/Z_{count}.json', 'w') as f:
#                  json.dump(data, f)
            with open(f'data/target/1_1.json', 'w') as f:
                json.dump(data, f)
            print(data)  
            data = [ [0] * gird_size for i in range(gird_size)]
            trian_data_set = get_data(trian_data_address,trian_file,trian_length)
            target_data_set = get_data(target_data_address,target_file,target_length)
            target = dic_separate(target_data_set)[0][0]
            no_deal_data = distance(trian_data_set,target,1)
            result_list = data_sort(no_deal_data,2)
            result = result_list[1]
            print(result_list)
        if(key2.value() == 0):#上
            if pointer.y-5 > draw_board[1]:
                pointer.y -= move_distance
            out = 0
        if(key4.value() == 0):#左
            if pointer.x-5 > draw_board[0]:
                pointer.x -= move_distance
            out = 0
        if(key3.value() == 0):#中
            out += 1
        if(key5.value() == 0):#下
            if pointer.y+5 < draw_board[2]:
                pointer.y += move_distance
            out = 0
        if(key6.value() == 0):#右
            if pointer.x+5 < draw_board[3]:
                pointer.x += move_distance
            out = 0
        
    time.sleep(1)
    LCD.fill(0xffff)






