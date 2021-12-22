# 导入模块
import pandas as pd  # 导入数据统计模块
import matplotlib  # 导入图表模块
import matplotlib.pyplot as plt  # 导入绘图模块
from sklearn.svm import LinearSVR  # 导入回归函数


class forecast:
    def get_clean(data):
        # 避免中文乱码
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符，使用rc配置文件来自定义
        # 简单清洗
        data = pd.read_csv(data)  # 读取csv数据
        data.dropna(axis=0, how='any', inplace=True)  # 删除data数据中的所有空值
        data['单价每平'] = data['单价每平'].map(lambda d: d.replace('元/平', ''))  # 将单价每平“元/平米”去掉
        data['单价每平'] = data['单价每平'].map(lambda d: d.replace(',', ''))  # 将单价每”平“元/平米去掉
        data['单价每平'] = data['单价每平'].astype(float)  # 将房子单价每平转换为浮点类型，float（data['',单价每平]）
        data['面积'] = data['面积'].map(lambda p: p.replace('平米', ''))  # 将面积“平米去掉”
        data['面积'] = data['面积'].astype(float)  # 将将面积转换为浮点类型
        return data

    # 获取价格预测
    def get_price_forecast(data):
        data_copy = data.copy()  # 拷贝数据
        print(data_copy[['空间', '面积']].head())
        data_copy[['室', '厅']] = data_copy['空间'].str.extract('(\d+)室(\d+)厅')
        data_copy['室'] = data_copy['室'].astype(float)  # 将房子室转换为浮点类型
        data_copy['厅'] = data_copy['厅'].astype(float)  # 将房子厅转换为浮点类型
        print(data_copy[['室', '厅']].head())  # 打印“室”、“厅”、“卫”数据

        del data_copy['空间']
        del data_copy['区域']
        del data_copy['地段']
        del data_copy['小区']
        del data_copy['朝向']
        del data_copy['装修']
        del data_copy['楼层']
        del data_copy['建成时间']
        del data_copy['单价每平']
        data_copy.dropna(axis=0, how='any', inplace=True)  # 删除data数据中的所有空值
        # 获取“建筑面积”小于300平米的房子信息
        new_data = data_copy[data_copy['面积'] < 500].reset_index(drop=True)
        print(len(new_data))
        print(new_data.head())  # 打印处理后的头部信息

        # 添加自定义预测数据
        new_data.loc[1944] = [173, None, 5.0, 2.0]
        new_data.loc[1945] = [163, None, 3.0, 1.0]
        data_train = new_data.loc[0:1943]
        x_list = ['面积', '室', '厅']  # 自变量参考列
        data_mean = data_train.mean()  # 获取平均值
        data_std = data_train.std()  # 获取标准偏差
        data_train = (data_train - data_mean) / data_std  # 数据标准化
        x_train = data_train[x_list].values  # 特征数据
        y_train = data_train['总价'].values  # 目标数据，总价
        linearsvr = LinearSVR(C=0.1)  # 创建LinearSVR()对象
        linearsvr.fit(x_train, y_train)  # 训练模型
        x = ((new_data[x_list] - data_mean[x_list]) / data_std[x_list]).values  # 标准化特征数据
        new_data[u'y_pred'] = linearsvr.predict(x) * data_std['总价'] + data_mean['总价']  # 添加预测房价的信息列
        print('真实值与预测值分别为：\n', new_data[['总价', 'y_pred']])
        y = new_data[['总价']][1900:]  # 获取2490以后的真实总价
        y_pred = new_data[['y_pred']][1900:]  # 获取2490以后的预测总价
        return y, y_pred  # 返回真实房价与预测房价

    # 显示预测房价折线图
    def broken_line(y, y_pred, title):
        '''
        y:y轴折线点，也就是房子总价
        y_pred,预测房价的折线点
        color：折线的颜色
        marker：折点的形状
        '''
        plt.figure()  # 图形画布
        plt.plot(y, color='r', marker='o', label='真实房价')  # 绘制折线，并在折点添加蓝色圆点
        plt.plot(y_pred, color='b', marker='*', label='预测房价')
        plt.xlabel('房子数量')
        plt.ylabel('房子总价')
        plt.title(title)  # 表标题文字
        plt.legend()  # 显示图例
        plt.grid()  # 显示网格
        plt.show()  # 显示图表

    def tansfer(data):
        clean = forecast.get_clean(data)
        x, y = forecast.get_price_forecast(clean)
        title = '房价预测分析'
        forecast.broken_line(x, y, title)


# if __name__ == '__main__':
#     data = 'cq_pre-owned_house2.csv'
#     forecast.tansfer(data)
if __name__ == '__main__':
    data = 'cq_pre-owned_house2.csv'
    forecast.tansfer(data)
