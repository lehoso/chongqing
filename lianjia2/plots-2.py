# 导入模块
import pandas as pd  # 导入数据统计模块
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


def get_district_averagePractice():
    group = data.groupby('区域')  # 将房子区域分组   先分组，再切片
    average_price_group = group['总价'].mean()  # 计算每个区域的均价,average_price_group字典  group['单价'].count()
    x = average_price_group.index  # 区域
    y = average_price_group.values  # 区域对应的均价
    return x, y  # 返回区域与对应的均价,region 二关   average_price均价


def get_hot_areaPlot(x, y, title):

    plt.figure()  # 图形画布
    plt.plot(x, y)
    plt.title(title, fontsize=20)  # 表标题文字
    plt.xlabel('区县')
    plt.ylabel('总价')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    x, y = get_district_averagePractice()
    title = '重庆各地区均价'
    get_hot_areaPlot(x, y, title)
