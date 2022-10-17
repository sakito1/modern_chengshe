#-*- coding: utf-8 -*
from Error import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from seaborn.matrix import heatmap  #绘制热力图
from pyecharts.charts import Map  #pyecharts绘制map,pie,themeriver,treemap
from pyecharts import options as opts
from pyecharts.charts import ThemeRiver
from pyecharts.charts import Geo, Pie, Timeline
from pyecharts.charts import TreeMap
from pyecharts import options as opts
from pyecharts.globals import ThemeType #引入主题
class visual:
    def __init__(self,pollutant):
        self.region = ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan',
                  'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong']
        self.region_CH=['朝阳区','昌平区','昌平区','东城区','西城区','石景山区','怀柔区','朝阳区','顺义区','东城区','海淀区','宣武区']
        self.pollutant = pollutant
        print("let's do it")

    def pie(self,region_dic):
        sum_li=[]
        name=[]
        for reg in self.region:
            data = region_dic[reg]
            da = list(zip(*data))  # 解码，分成时间序列和数值,对于tuple是无法做索引的
            shuzhi = np.array([float(i) for i in da[1]])#转为tuple类型才能求和
            sum_li.append(sum(shuzhi))
            name.append(reg)#以防提取名字的时候出问题，因为字典是不按顺序的
        pie=Pie()
        pie.add("",[list(z) for z in zip(name,sum_li)])
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c} {d}%"))#设置格式
        pie.set_global_opts(title_opts=opts.TitleOpts(title=f"各地{self.pollutant:}占比"))
        pie.render(f"./{self.pollutant:} pie.html")

    def line(self,region_dic):#传入的是北京各地的某污染物的线图
        plt.figure(figsize=(24,18))
        i=1
        for reg in self.region:
            data=region_dic[reg]
            da=list(zip(*data))#解码，分成时间序列和数值,对于tuple是无法做索引的
            time=da[0]
            shuzhi=[float(i) for i in da[1]]
            plt.subplot(3,4,i)
            plt.plot(time,shuzhi)
            plt.title(f"{reg:}\'s {self.pollutant:}")
            plt.xticks(fontsize=6)
            i+=1
        plt.savefig(f"./beijing regions of {self.pollutant:} line")
        plt.show()#这个放保存后面不然存不进去,不知道为啥


    def river(self):
        pass

    def map(self,map_dic):
        region=self.region
        data={}
        for j in range(len(region)):
            da=map_dic[region[j]]
            med=0
            for i in range(len(da)):
                med+=float(da[i]['AQI'])
            mean=med/len(da)
            if data.get(self.region_CH[j],0)!=0:#有些区有重复就很烦
                data[self.region_CH[j]]=(mean+data.get(self.region_CH[j],0))/2
            else:
                data[self.region_CH[j]]=mean
        data=list(zip(data.keys(),data.values()))
        map=Map(init_opts=opts.InitOpts(width='900px',height='800px',theme=ThemeType.DARK))
        map.add('AQI',data,maptype='北京')
        map.set_global_opts(title_opts=opts.TitleOpts(title='北京各地AQI'),visualmap_opts=opts.VisualMapOpts(max_=150,min_=90,split_number=6,range_text="AQI颜色区间"))
        map.render("./Map.html")


    def correlation(self,C_Matrix):#传入一个dataframe的字典列表
        key=list(C_Matrix.keys())
        plt.figure(figsize=(24,18))
        for i in range(len(C_Matrix)):
            plt.subplot(3,4,i+1)
            heatmap(C_Matrix[key[i]],annot=False)
            plt.title(f"{key[i]:}heatmap of correlation",fontsize=10)
            cax = plt.gcf().axes[-1]
            cax.tick_params(labelsize=5)  # colorbar刻度字体大小
            plt.tick_params(labelsize=5)#设置刻度大小
        plt.savefig("./北京各地热力图.png")
        plt.show()