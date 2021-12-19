import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 写入MySQL中
import pymysql
from sqlalchemy import create_engine

pymysql.install_as_MySQLdb()

# 表头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
}
# 存入数据
a = []


# 得到整个网页所有数据
def get_info(url):
    # 获取内容
    wb_data = requests.get(url, headers=header)
    # 以lxml树格式读取
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # 关注度
    fllowInfo = soup.select('div.followInfo')
    # 主城区域
    district = soup.select('div.position > dl> dd > div > div > a.selected')
    # 地理位置
    positionInfo = soup.select('div.info.clear > div.flood > div')
    # 总价
    totalPrice = soup.select('div.totalPrice.totalPrice2 > span')
    # 单价
    unitPrice = soup.select('div.unitPrice > span')
    # 详细位置
    houseInfo = soup.select(' div.info.clear > div.address > div')
    # 标题
    title = soup.select('div.title > a')
    # print(positionInfo)
    # 每个区域单独叠加
    for district, in zip(district):
        districts = {
            '区域': district.get_text().strip()
        }

    # 存入字段数据
    for title, fllowInfo, positionInfo, houseInfo, unitPrice, totalPrice in zip(title, fllowInfo, positionInfo,
                                                                                houseInfo, unitPrice,
                                                                                totalPrice):
        fllowInfos = fllowInfo.get_text().split('/')
        positionInfos = positionInfo.get_text().split('-')
        houseInfos = houseInfo.get_text().split('|')
        titles = title.get_text().strip()
        data = {
            '标题': titles.strip(),
            '地段': positionInfos[1].strip(),
            '小区': positionInfos[0].strip(),
            '空间': houseInfos[0].strip(),
            '面积': houseInfos[1].strip(),
            '朝向': houseInfos[2].strip(),
            '装修': houseInfos[3].strip(),
            '楼层': houseInfos[4].strip(),
            '建成时间': (houseInfos[-3].strip() if len(houseInfos) > 7 else houseInfos[-2].strip()) if len(
                houseInfos) > 6 else '',
            '构筑物': (houseInfos[-2].strip() if len(houseInfos) > 7 else houseInfos[-1].strip()) if len(
                houseInfos) > 6 else houseInfos[-1].strip(),
            '单价每平': unitPrice.get_text().strip(),
            '总价': totalPrice.get_text().strip(),
            '关注': fllowInfos[0].strip(),
            '距今发布日期': fllowInfos[1].strip(),
        }
        data.update(districts)
        a.append(data)
        print(data)


if __name__ == '__main__':
    # 打算爬取哪几个区域
    cqArea = ['jiangbei', 'yubei', 'nanan', 'banan', 'shapingba',
              'jiulongpo', 'yuzhong', 'dadukou', 'beibei', 'fuling',
              'bishan']
    for i in range(len(cqArea)):
        for j in range(1, 10):
            urls = [
                'https://cq.lianjia.com/ershoufang/{}/pg{}/'.format(cqArea[i], str(j))
            ]
            for url in urls:
                get_info(url)
                # time.sleep(1)
# pandas存入数据
df_out = pd.DataFrame(a, columns=[
    '标题', '区域', '地段', '小区', '空间', '面积',
    '朝向', '装修', '楼层', '建成时间', '构筑物',
    '单价每平', '总价', '关注', '距今发布日期'
])
df_out.to_csv('cq_pre-owned_house.csv', index=False, index_label=False)
# # 写入MySQL中
conn = create_engine('mysql+mysqldb://root:000000@localhost:3306/keshihua?charset=utf8')
# index为索引号，index_label下标
df_out.to_sql(name='cq_pre-ownedHouse', con=conn, if_exists='append', index=False, index_label=False)
