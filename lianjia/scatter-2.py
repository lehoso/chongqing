import pandas as pd
import numpy as np
import matplotlib  # 导入图表模块

import matplotlib.pyplot as plt  # 导入绘图模块

# 避免中文乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei显示中文
matplotlib.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符，使用rc配置文件来自定义
# 简单清洗
data = pd.read_csv('cq_pre-owned_house2.csv')  # 读取csv数据
# del data['Unnamed: 0']  # 将索引列删除
data.dropna(axis=0, how='any', inplace=True)  # 删除data数据中的所有空值
data['单价每平'] = data['单价每平'].map(lambda d: d.replace('元/平', ''))  # 将单价每平“元/平米”去掉
data['单价每平'] = data['单价每平'].map(lambda d: d.replace(',', ''))  # 将单价每”平“元/平米去掉
data['单价每平'] = data['单价每平'].astype(float)  # 将房子单价每平转换为浮点类型，float（data['',单价每平]）
data['面积'] = data['面积'].map(lambda p: p.replace('平米', ''))  # 将面积“平米去掉”
data['面积'] = data['面积'].astype(float)  # 将将面积转换为浮点类型



def get_hot_areaPractice():
    group = data.groupby('地段')  # 将房子区域分组
    average_price_group = group['总价'].mean().sort_values(ascending=False).head(20)  # 计算每个区域的均价，average_price_group字典
    x = average_price_group.index  # 区域
    y = average_price_group.values.astype(int)  # 区域对应的均价a =['t':'123'] a.keys()
    return x, y


def get_hot_areaScatter(x, y, title):
    colors = y * 100
    area = y * 1  # 根据y值的大小生成不同形状
    print(colors)
    # c=colors,marker="o",s=area
    # alpha=0.3
    plt.scatter(y, x, c=colors, marker="o", s=area, alpha=0.5)
    plt.colorbar()  # 绘制颜色对照条
    plt.title(title, fontsize=20)  # 表标题文字
    plt.xlabel('总价：万')
    plt.ylabel('十佳地段')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    x, y = get_hot_areaPractice()
    title = '重庆最佳地段总价'
    get_hot_areaScatter(x, y, title)

#https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_with_legend.html#sphx-glr-gallery-lines-bars-and-markers-scatter-with-legend-py