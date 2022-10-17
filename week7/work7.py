from Analysis import *
import pandas as pd
import numpy as np
from Visualization import *

def examine():#检查是否有空值
    region = ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan',
              'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong']
    for item in region:
        data = pd.read_csv(f"./PRSA_Data_20130301-20170228/PRSA_Data_{item:}_20130301-20170228.csv")
        name = data.columns.values.tolist()  # 列名称
        x, y = np.where(data.isnull())
        x = list(x)
        y = list(y)
        if len(x) > 0:  # 说明有异常值
            try:
                pollutant = name[y[0]]
                year = data['year'][x[0]]
                region = "Aotizhongxin"
                month = data['month'][x[0]]
                day = data['day'][x[0]]
                hour = data['hour'][x[0]]
                raise NotNumError_new(region, year, month, day, hour,pollutant)  # 之前使用NotNumError的时候，一直报错，说不显示属性，可能存在重名等问题，因此改了个名字就成功了

            except NotNumError_new as e:  # 认为捕获错误，同时对类实例化
                print(e.message)
            # #下列函数块能够把所有的na的位置打印出来，但是如果全部打印出来会很乱，因此我只打印第一个na
            # for i in range(len(x)):
            #     try:
            #         pollutant=name[y[i]]
            #         year=data['year'][x[i]]
            #         region="Aotizhongxin"
            #         month=data['month'][x[i]]
            #         day=data['day'][x[i]]
            #         hour=data['hour'][x[i]]
            #         raise NotNumError_new(region, year, month, day,hour,pollutant)#之前使用NotNumError的时候，一直报错，说不显示属性，可能存在重名等问题，因此改了个名字就成功了
            #
            #     except NotNumError_new as e:#认为捕获错误，同时对类实例化
            #         print(e.message)

        data.fillna(method='pad', inplace=True)#利用前后值补足,对于还没补全的直接变成0，此时变成0的已经很少了
        data.fillna('0',inplace=True)#此时完美解决空值问题
        try:
            data.to_csv(f"./PRSA_Data_20130301-20170228/{item:}.csv", index=False,
                        sep=',')  # 在调试的时候，由于该函数不支持覆写，因此采用try，当之前已经完成了na值补全的文件时，则跳过报错，继续运行下一个
        except:
            continue

def data(pollutant):#展示数据
    river={}
    place=['Aotizhongxin','Changping','Dingling','Dongsi','Guanyuan','Gucheng','Huairou','Nongzhanguan','Shunyi','Tiantan','Wanliu','Wanshouxigong']
    for reg in place:
        B_R=Region(reg,pollutant)
        river[reg]=B_R.read()#将所有数值保存在字典中
    Ana_P=Province('2013-3-1-0','2015-3-1-0')
    Ana_C=Cor()
    Ana_P_data=Ana_P.Time_Region()
    Ana_C_data=Ana_C.analysis()
    # print(river)
    # print(Ana_P_data)
    # print(Ana_C_data)
    return river,Ana_P_data,Ana_C_data

def Vis(R,P,C,pollutant):#可视化
    Graph=visual(pollutant)
    #Graph.correlation(C)#相关系数热力图
    #Graph.line(R)
    #Graph.pie(R)
    Graph.map(P)#传入map的数据




def main():
    #examine()
    R,P,C=data("SO2")#以二氧化硫为例，我们希望输出的是单个地区，所有地区的
    Vis(R,P,C,"SO2")

if __name__ == '__main__':
    main()