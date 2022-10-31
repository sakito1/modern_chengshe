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
            ##如果不执行return则不会运行func函数，如果return则会运行func函数，对于前面wrapper函数里的操作可以起到装饰函数的作用
        return wrapper
@storage('./store.txt')
def myfunc():
    for i in range(100000):
        st=str(i)
        print(st)