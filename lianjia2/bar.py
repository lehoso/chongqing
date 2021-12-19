# 导入模块
import pandas as pd  # 导入数据统计模块
import matplotlib  # 导入图表模块
import matplotlib.pyplot as plt  # 导入绘图模块

# 定义为柱状图类
class bar:
    # 对data数据清洗
    def get_clean(data):
        # 避免中文乱码
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符，使用rc配置文件来自定义
        # 简单清洗
        # data = pd.read_csv('cq_pre-owned_house2.csv')  # 读取csv数据
        data = pd.read_csv(data)  # 读取csv数据
        data.dropna(axis=0, how='any', inplace=True)  # 删除data数据中的所有空值
        data['单价每平'] = data['单价每平'].map(lambda d: d.replace('元/平', ''))  # 将单价每平“元/平”去掉
        data['单价每平'] = data['单价每平'].map(lambda d: d.replace(',', ''))  # 将单价中小数点去掉
        data['单价每平'] = data['单价每平'].astype(float)  # 将房子单价每平转换为浮点类型，float（data['',单价每平]）
        data['面积'] = data['面积'].map(lambda p: p.replace('平米', ''))  # 将面积“平米去掉”
        data['面积'] = data['面积'].astype(float)  # 将将面积转换为浮点类型
        return data


    # 获取各区热门户型分析，根据需求，，进一步处理数据，如果要写相应算法，需要根据算法所需求的数据处理
    def get_hot_portal(data):
        group = data.groupby('空间')  # 将房子区域分组
        a = group['空间'].count().sort_values(ascending=False).head()  # 计算最热门的户型
        b = group['单价每平'].mean()[a.index]  # 区域对应的均价a =['t':'123'] a.keys()
        x = b.index
        y = b.values.astype(int)
        return x, y  # 返回区域与对应的户型和价格

    # 显示均价横条形图
    def hot_portal_barh(x, y, title):
        plt.figure()  # 图形画布
        plt.barh(x, y, alpha=0.9, color='red')  # 绘制条形图
        plt.xlabel("均价")  # 区域文字
        plt.ylabel("户型")  # 均价文字
        plt.title(title)  # 表标题文字
        plt.xlim(0, 20000)  # X轴的大小
        # 为每一个图形加数值标签
        for y, x in enumerate(y):
            plt.text(x + 100, y, str(x) + '元/平', ha='left')
        plt.show()

    def transfer(data):
        clean = bar.get_clean(data)
        x, y = bar.get_hot_portal(clean)
        title = '热门户型均价分析'
        bar.hot_portal_barh(x, y, title)

# if __name__ == '__main__':
#     x, y = get_hot_portal(self,data)
#     title = '热门户型均价分析'
#     hot_portal_barh(x, y, title)
