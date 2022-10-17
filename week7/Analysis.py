import csv
import openpyxl
from Error import *
import csv
import datetime
import numpy as np
import pandas as pd

#一开始不如用pandas库里的read_csv，直接对dataframe类型进行处理
class Region:#该类分析的是某区域的污染物数据
    def __init__(self,region,pollutant):
        self.region = region
        self.pollutant = pollutant

    def read(self):
        with open("./PRSA_Data_20130301-20170228/{:}.csv".format(self.region), "r") as f:
            file = csv.DictReader(f)  # 转为字典的格式列表，每一行表示一个字典
            file=list(file)#很多类型都不支持一些调用，先转为列表比较方便
            data=[]
            if self.pollutant in file[0].keys():
                for row in file:
                    time=datetime.datetime(year=int(row["year"]),month=int(row['month']),day=int(row['day']),hour=int(row['hour']))
                    li=[time,row[self.pollutant]]
                    data.append(li)#deposit data
            else:
                print("you enter the wrong pollutant")
        return(data)#返回一个列表包含了时间和污染物的数据


class Province:
    def __init__(self,*args):#输入一个时间或者时间段
        self.args = args

    def __AQI(self,PM2_5, PM10, SO2, NO2, CO, O3):  # 注意在拼盘IQA时，CO单位用的是mg
        """此为1h的AQI计算代码，24h的只需要更换Idata即可"""
        qua = [0, 50, 100, 150, 200, 300, 400, 500]
        data = [PM2_5, PM10, SO2, NO2, CO / 1000, O3]
        IAQI = list(np.zeros(6))
        Idata = [
            [0, 35, 75, 115, 150, 250, 350, 500],  # PM2.5 1小时平均
            [0, 50, 150, 250, 350, 420, 500, 600],  # （PM10）1小时平均
            [0, 150, 500, 650, 800],  # so2
            [0, 100, 200, 700, 1200, 2340, 3090, 3840],  # no2
            [0, 5, 10, 35, 60, 90, 120, 150],  # co
            [0, 160, 200, 300, 400, 800, 1000, 1200]  # o3
        ]
        for i in range(len(Idata)):
            POL = data[i]  # 提取第i种污染物的数值
            # 寻找区间
            for j in range(len(Idata[i])):
                if Idata[i][j] >= POL:
                    break  # 此时找到污染物的上界,且记录上界的位置，此时对应分值表的上界
            iqa = round((qua[j] - qua[j - 1]) / (Idata[i][j] - Idata[i][j - 1]) * (POL - Idata[i][j - 1]) + qua[j - 1])
            IAQI[i] = iqa
        IAQI = np.array(IAQI)
        AQI = max(IAQI)
        return (AQI)

    def Time_Region(self):
        region=['Aotizhongxin','Changping','Dingling','Dongsi','Guanyuan','Gucheng','Huairou','Nongzhanguan','Shunyi','Tiantan','Wanliu','Wanshouxigong']
        region_dic={}
        for place in region:
            with open("./PRSA_Data_20130301-20170228/{:}.csv".format(place),"r") as f:
                file = csv.DictReader(f)  # 转为字典的格式列表，每一行表示一个字典
                file = list(file)  # 很多类型都不支持一些调用，先转为列表比较方便
                shuju=[]#该地区所有数据
                if len(self.args)==1:#表示时间点
                    ar=self.args#注意调用的时候是self.args
                    args=ar[0].split('-')
                    for row in file:
                        content={}#每一个数据存在一个字典里
                        if row['year']==args[0] and row['month']==args[1] and row['day']==args[2] and row['hour']==args[3]:#匹配时间点
                            content['time']=datetime.datetime(year=int(row["year"]),month=int(row['month']),day=int(row['day']),hour=int(row['hour']))
                            content['PM2.5']=row['PM2.5']
                            content['PM10']=row['PM10']
                            content['SO2']=row['SO2']
                            content['NO2']=row['NO2']
                            content['CO']=row['CO']
                            content['O3']=row['O3']
                            content['TEMP']=row['TEMP']
                            content['PRES']=row['PRES']
                            content['DEWP']=row['DEWP']
                            content['WSPM']=row['WSPM']
                            content['RAIN']=row['RAIN']
                            content['wd']=row['wd']
                            AQI=self.__AQI(float(row['PM2.5']),float(row['PM10']),float(row['SO2']),float(row['NO2']),float(row['CO']),float(row['O3']))
                            content['AQI']=AQI
                            shuju.append(content)#插入每条数据
                elif len(self.args) == 2:  # 表示时间段
                    start=self.args[0].split("-")#直接转数字计算
                    end=self.args[1].split("-")
                    start=int(start[0])*1000000+int(start[1])*10000+int(start[2])*100+int(start[3])
                    end=int(end[0])*1000000+int(end[1])*10000+int(end[2])*100+int(end[3])
                    for row in file:
                        content ={}
                        #以2013 03 10 0为例
                        time=int(row['year'])*1000000+int(row['month'])*10000+int(row['day'])*100+int(row['hour'])
                        if time<=end and time>=start:
                            content['time'] = datetime.datetime(year=int(row["year"]), month=int(row['month']), day=int(row['day']),
                                                                hour=int(row['hour']))
                            content['PM2.5'] = row['PM2.5']
                            content['PM10'] = row['PM10']
                            content['SO2'] = row['SO2']
                            content['NO2'] = row['NO2']
                            content['CO'] = row['CO']
                            content['O3'] = row['O3']
                            content['TEMP'] = row['TEMP']
                            content['PRES'] = row['PRES']
                            content['DEWP'] = row['DEWP']
                            content['WSPM'] = row['WSPM']
                            content['RAIN'] = row['RAIN']
                            content['wd'] = row['wd']
                            AQI = self.__AQI(float(row['PM2.5']), float(row['PM10']), float(row['SO2']),
                                             float(row['NO2']), float(row['CO']), float(row['O3']))
                            content['AQI'] = AQI
                            shuju.append(content)#放在里面是为了防止加入空的字典
                else:
                    print("wrong number of time")
            region_dic[place]=shuju
        return(region_dic)#返回各个地区在这个时间段的数据

class Cor:
    def __init__(self):
        self.region=['Aotizhongxin','Changping','Dingling','Dongsi','Guanyuan','Gucheng','Huairou','Nongzhanguan','Shunyi','Tiantan','Wanliu','Wanshouxigong']

    def analysis(self):
        relation_cor={}
        for i in self.region:
            data = pd.read_csv(f"./PRSA_Data_20130301-20170228/{i:}.csv")
            new = data.iloc[:, [i for i in range(5, 17)]]#提取属性所在的列的序号，利用iloc返回部分数据框
            matrix = new.corr("spearman")
            relation_cor[i]=matrix
        return relation_cor#返回各地的构成,字典形式展示