#%%
import copy
from queue import PriorityQueue
from random import randint
import numpy as np
class State:
    def __init__(self, data=None, par=None, g=0, h=0, op=None):
        self.data = data  # data:dữ liệu mảng 1 chiều
        self.par = par  # par: nút cha
        self.g = g  # g: trọng số đường đi từ cái đỉnh xuất phát đến đỉnh hiện tại
        self.h = h  # h: hàm dánh giá đỉnh hiện tại so với điểm đích
        self.op = op #op: Toán tử ở trên state

    def clone(self):
        #Tạo hàm copy: Copy từ self sang một trạng thái mới (sn)
        sn = copy.deepcopy(self)
        return sn
  
    def Key(self):
        # Key: Với mỗi trạng thái cộng tất cả phần tử lại theo từ trái sang phải, từ trên xuống dưới. Cộng theo chuỗi
        if self.data == None:
            return None
        res = ''
        for x in self.data:
            res += (str)(x)
        return res

    def __lt__(self, other):
        # lt: hàm nào nhỏ cho lên phía trên
        if other == None:
            return False
        return self.g + self.h < other.g + other.h

    def __eq__(self, other):
    	# Định nghĩa 2 Key value bằng nhau: 
        if other == None:
            return False
        return self.Key() == other.Key()

G = None
S = None
class Operator:
    count = []
    def __init__(self, i):
        self.i = i
        #Truyền vào một biến i: Nếu:
        	# i=0: action Up
        	# i=1: action Down
        	# i=2: action Left
        	# i=3: action Right
        #Kiểm tra trạng thái data s
        	#Nếu null => none
        #Tìm vị trí 0 ở hàng x cột y trong trạng thái s
        #hoán đổi vị trí x, y theo self.i ( i=0 || i=1 || i=2 || i=3 )
    def Up(self, s):
        if self.checkStateNull(s):
            return None
        x, y = self.findPos(s)
        if (x == 2):  # nếu vị trí số 0 ở hàng 2 (chữ số 0 hàng cuối xét từ dưới lên {0, 1, 2}) => không Up được
            return None
        return self.swap(s, x, y, self.i)

    def Down(self, s):
        if self.checkStateNull(s):
            return None
        x, y = self.findPos(s)
        if x == 0:  # nếu vị trí số 0 ở hàng 0  => None (0, 1, 2) vì không di chuyển xuống được
            return None
        return self.swap(s, x, y, self.i)

    def Left(self, s):
        if self.checkStateNull(s):
            return None
        x, y = self.findPos(s)
        if y == 2:  # nếu vị trí số 0 ở cột 2 => None (0, 1, 2) vì không di chuyển trái được
            return None
        return self.swap(s, x, y, self.i)

    def Right(self, s):
        if self.checkStateNull(s):
            return None
        x, y = self.findPos(s)
        if y == 0:  # nếu vị trí số 0 ở cột 0 => None (0, 1, 2) vì không di chuyển phải được
            return None
        return self.swap(s, x, y, self.i)

    def Move(self, s):
        #Hàm di chuyển trang thái s
        if self.i == 0:
            return self.Up(s)
        if self.i == 1:
            return self.Down(s)
        if self.i == 2:
            return self.Left(s)
        if self.i == 3:
            return self.Right(s)
        return None

    
    def checkStateNull(self, s):
        # Hàm kiểm tra trạng thái s có Null không . nếu có trả về None
        return s.data == None

    def swap(self, s, x, y, i):
        #Hàm hoán đổi vị trí 
        sz = 3
        sn = s.clone()
        x_new = x
        y_new = y
        # xet up, down
        if (i == 0): #UP
            x_new = x + 1
            y_new = y
        if i == 1: #DOWN
            x_new = x - 1
            y_new = y
        # xet left, right
        if i == 2: #LEFT
            x_new = x
            y_new = y + 1
        if i == 3: #RIGHT
            x_new = x
            y_new = y - 1
        sn.data[x * sz + y] = s.data[x_new * sz + y_new] #hoán đổi phần tử
        sn.data[x_new * sz + y_new] = 0 #gán x_new & y_new = 0
        return sn

    
    def findPos(self, s):
        # hàm tìm vị trí số 0 trong trạng thái s
        sz = 3
        for i in range(sz):
            for j in range(sz):
                if s.data[i * sz + j] == 0:
                    return i, j
        return None

    def checkInPriority(Open, tmp):
    	# Kiểm tra mảng thuộc Open 

        if (tmp == None):
            return False
        return (tmp in Open.queue)

    def equal(O, G):
        if O == None:
            return False
        return O.Key() == G.Key()

    def Path(O):
    	#Kiểm tra parent có khác NULL không : 
    	# In action phần tử thứ i
        len = ['DOWN', 'UP', 'RIGHT', 'LEFT']
        if O.par != None:
            Operator.Path(O.par)
            print(len[O.op.i], end = ' ')

    
    def Hx(S, G):
        # Số vị trí khác nhau hiện tại của trạng thái S so với trạng thái G
        sz = 3
        res = 0
        for i in range(sz):
            for j in range(sz):
                if S.data[i * sz + j] != G.data[i * sz + j]:
                    res += 1
        return res

    def Run():
    	#thuật toán A*
        Open = PriorityQueue()
        Closed = PriorityQueue()
        S.g = 0
        S.h = Operator.Hx(S, G) #Hàm Hx: của trạng thái S so với trạng thái G
        Open.put(S)
        while True:
            if Open.empty():
                print('tim kiem that bai')
                break
            O = Open.get()
            Closed.put(O)
            if Operator.equal(O, G) == True:
            	#Kiểm tra trạng thái O bằng trạng thái đích
                print('TÌM THẤY SOLUTION:')
                Operator.Path(O)
                break
            # tìm tất cả trạng thái còn lại
            for i in range(4):
                op = Operator(i) #xét op theo Operator theo i (i=0: Up, i=1: Down, i=2: Left, i=3: Right)
                child = op.Move(O)
                if child == None:
                	#Nếu trạng thái con Null => bỏ qua
                    continue
                ok1 = Operator.checkInPriority(Open, child) #Kiểm tra ok1 có thuộc bất cứ con nào hay không
                ok2 = Operator.checkInPriority(Closed, child)
                if not ok1 and not ok2:
                    child.par = O
                    child.op = op
                    child.g = O.g + 1
                    child.h = Operator.Hx(child, G)
                    Open.put(child)

    def init(num):
    	#tạo trạng thái G
    	# Cấp phát vùng nhớ cho data
    	#tạo dữ liệu gồm 9 số random theo mảng
        G = State()
        sz = 3
        G.data = []
        for i in range(sz):
            for j in range(sz):
                G.data.append((i * sz + j + 0) % 9)

        S = G.clone()
        for i in range(num):
            op = Operator(randint(0, 3))
            tmp = op.Move(S)
            if tmp != None:
                S = tmp
        return S, G

# %%
