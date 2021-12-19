# 导入模块
import pandas as pd  # 导入数据统计模块
import matplotlib  # 导入图表模块
import matplotlib.pyplot as plt  # 导入绘图模块


class plots:
    def get_clean(data):
        # 避免中文乱码
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符，使用rc配置文件来自定义
        # 简单清洗
        # data = pd.read_csv('cq_pre-owned_house2.csv')  # 读取csv数据
        data = pd.read_csv(data)
        data['单价每平'] = data['单价每平'].map(lambda d: d.replace('元/平', ''))  # 将单价每平“元/平米”去掉
        data['单价每平'] = data['单价每平'].map(lambda d: d.replace(',', ''))  # 将单价每”平“元/平米去掉
        data['单价每平'] = data['单价每平'].astype(float)  # 将房子单价每平转换为浮点类型，float（data['',单价每平]）
        data['面积'] = data['面积'].map(lambda p: p.replace('平米', ''))  # 将面积“平米去掉”
        data['面积'] = data['面积'].astype(float)  # 将将面积转换为浮点类型
        data['建成时间'] = data['建成时间'].map(lambda p: p.replace('年建', ''))  # 将面积“平米去掉”
        data['建成时间'] = data['建成时间'].astype(int)  # 将将面积转换为浮点类型
        return data

    def get_buildyears_averagePractice(data):
        group = data.groupby('建成时间')
        average_price_group = group['总价'].mean()  # 计算每个区域的均价，average_price_group字典
        x = average_price_group.index  # 区域
        y = average_price_group.values.astype(int)  # 区域对应的均价a =['t':'123'] a.keys()
        return x, y

    def get_hot_areaPlot(x, y, title):
        plt.figure()  # 图形画布
        plt.plot(x, y)
        plt.title(title, fontsize=20)  # 表标题文字
        plt.xlabel('房屋建成时间')
        plt.ylabel('当年平均价 / 万')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

    def transfer(data):
        clean = plots.get_clean(data)
        x, y = plots.get_buildyears_averagePractice(clean)
        title = '重庆近几十年建成均价走势图'
        plots.get_hot_areaPlot(x, y, title)

# if __name__ == '__main__':
#     x, y = get_buildyears_averagePractice()
#     title = '重庆近几十年建成均价走势图'
#     get_hot_areaPlot(x, y, title)
