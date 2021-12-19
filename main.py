from lianjia2.bar import *
from lianjia2.pie import *
from lianjia2.plots import *
from lianjia2.scatter import *
from lianjia2.recommendation import *
from lianjia2.forecast import *

if __name__ == '__main__':
    # 六个图像显示
    data = 'cq_pre-owned_house2.csv'
    bar.transfer(data)
    pie.transfer(data)
    plots.transfer(data)
    scatter.transfer(data)
    forecast.tansfer(data)
    recommendation.tansfer(data)
