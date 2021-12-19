import pandas as pd
import numpy as np
import matplotlib  # 导入图表模块

import matplotlib.pyplot as plt  # 导入绘图模块


class scatter:
    def get_clean(data):
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
        return data

    def get_district_describe(data):
        group = data.groupby('区域')  # 将房子区域分组
        average_price_group = group['单价每平'].describe()  # 计算每个区域的均价，average_price_group字典
        x = average_price_group.index
        y = average_price_group
        return x, y

    def district_describe_scatter(x, y, title):
        area = y['std'].values * 0.05  # 根据y值的大小生成不同形状
        plt.figure()  # 图形画布
        plt.scatter(x, y['max'], label='最大值', s=area, c='r', alpha=0.5)
        plt.scatter(x, y['mean'], label='均值', s=area, c='y', alpha=0.5)
        plt.scatter(x, y['min'], label='最小值', s=area, c='g', alpha=0.5)
        plt.title(title, fontsize=20)  # 表标题文字
        plt.colorbar()  # 绘制颜色对照条
        plt.xlabel('房屋建成时间')
        plt.ylabel('当年平均价 / 万')
        plt.xticks(rotation=45)
        plt.legend(loc="upper left", title="Classes")
        plt.show()

    def transfer(data):
        clean = scatter.get_clean(data)
        x, y = scatter.get_district_describe(clean)
        title = '重庆各区域描述解析分布'
        scatter.district_describe_scatter(x, y, title)

# if __name__ == '__main__':
#     x, y = scatter.get_district_describe()
#     title = '重庆各区域描述解析分布'
#     scatter.district_describe_scatter(x, y, title)


# https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_with_legend.html#sphx-glr-gallery-lines-bars-and-markers-scatter-with-legend-py
