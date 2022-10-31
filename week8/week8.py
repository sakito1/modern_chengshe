import functools
from functools import wraps
from functools import reduce
import sys
from memory_profiler import profile
from line_profiler import LineProfiler
from tqdm import tqdm
import os
import time
from playsound import playsound



#检查是否存在相应路径
def path_examine(path,func):
    @wraps(func)
    def wrapper(*args,**kwargs):
            if os.path.exists(path)==True:
                print("path already exists")
            else:
                os.mkdir(path)
                print("creating the path")
            return func(*args,**kwargs)
    return wrapper
'''
path="./store.txt"
path2="./ss.txt"
ex1=functools.partial(path_examine,path)
ex2=functools.partial(path_examine,path2)
@ex1
def pri(path):
    print(path)
pri(path)
@ex2
def pri(path):
    print(path)
pri(path2)
'''

#使用类来实现声音提醒代码处理
class Music:
    def __init__(self):
        pass
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            a=func(*args, **kwargs)
            if isinstance(a,str):
                playsound('./str.mp3')
            elif isinstance(a,int):
                playsound('./num.mp3')
            else:
                playsound("./els.mp3")
        return wrapper
'''
@Music()
def fun1():
    for i in range(4):
        print(i)
    print(type(i))
    return i
fun1()
time.sleep(5)

@Music()
def fun2():
    for i in 'abcdef':
        print(i)
    print(type(i))
    return i
fun2()
time.sleep(5)

@Music()
def fun3():
    dic={'1':1, '2':2, '3':3, '4':4}
    dic=zip(dic.keys(),dic.values())
    for i in dic:
        print(i)
    print(type(i))
    return i
fun3()
time.sleep(5)
'''
'''
#保存打印结果的装饰器
class storage:
    def __init__(self,path):
        self.path=path
    def __call__(self,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            __console=sys.stdout#保存屏幕的sys.out
            info='Info:'+func.__name__+" was called"
            with open(self.path,'a') as f:
                f.write(info+'\n')
                sys.stdout=f#将打印位置定位到文件中
                func(*args,**kwargs)
            sys.stdout=__console#还原位置
            return func(*args,**kwargs)
            ##如果需要使用func函数则返回函数即可，如果不需要使用则不返回也行
        return wrapper
@storage('./store.txt')
def myfunc():
    for i in range(100000):
        st=str(i)
        print(st)
#进行代码进度与时间的显示
myfunc()
'''
class Vis:
    def __init__(self):
        pass
    @profile#该方法使用的是命令行操作
    def test_time(self):
        for i in range(100):
            a=[1]*(10**6)
            b=[2]*(10**5)

    def sum(self,x,y):
        return x+y

    def mult(self,x,y):
        return x*y

    def ceshi(self):
        lis=[1]*(10**6)
        a=reduce(self.mult,lis)
        b=reduce(self.sum,lis)
        return a,b

    def jin_du(self):#显示进度条
        lis=[1]*(10**3)
        bar=tqdm(lis)#转化成进度条的形式，跑了多少将会返回在进度条中
        j = 1
        for i in bar:##遍历表示跑了多少进度条
            bar.set_description("Now get "+"No.".format(j))
            j=j+1
            time.sleep(0.001)

t=Vis()
t.jin_du()
a,b=t.ceshi()
print(a)
print(b)
lp = LineProfiler()
lp_wrapper = lp(t.ceshi)
lp_wrapper()#
lp.print_stats()