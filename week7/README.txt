原始数据说明：
各类污染物都是微克/立方米，但是在计算AQI时CO是使用毫克的
原始数据的格式分布：
['No', 'year', 'month', 'day', 'hour', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM', 'station']
Region类的数据格式
{地区:[时间,污染物数据]}
Province类的数据格式关于时间的输入
["year-month-day-hour","year-month-day-hour"]
Province类返回的数据
{region:{time:,各类数值，AQI的值}
region包含的地区
['Aotizhongxin','Changping','Dingling','Dongsi','Guanyuan','Gucheng','Huairou','Nongzhanguan','Shunyi','Tiantan','Wanliu','Wanshouxigong']
有几个地方地图上貌似找不到，用区来试一试,区也不太好使，有几个地方一个区orz

cor_relation返回的是每个地区的污染属性与天气情况的相关系数的dataframe构成的字典


关于Visualization模块，我设计了一个Visual类，关于visual类有以下函数：
pie 饼图，对每种属性在这个时间段内的均值做一个饼图？有待考量，貌似不是那么的合理
line 线图 对于某地某污染物的数值做线图
river 河流图 对各地的污染物变化水平做河流图,暂时不太想做，不急
correlation 每个地区的相关系数热力图
map 对每个地区的污染物分布情况做一个地图
给污染情况做一个权值的处理，然后在地图上展示？
计算AQI，然后对每个时刻的AQI做一个均值，然后将这个值在北京地图上表示出来。

关于data输出的值分别为某种污染物的所有地区数值字典，北京某时间段的各地污染物数值字典，北京各地的污染物相关系数字典
