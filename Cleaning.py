import pandas as pd

# 写入MySQL中
import pymysql
from sqlalchemy import create_engine

df = pd.read_csv(r'lianjia2/cq_pre-owned_house.csv', encoding='utf-8')

df_clean = df.drop_duplicates(subset='标题', keep='first')  # 主键 关键字段，删除
print(len(df_clean))

df_clean = df_clean.dropna()  # 1.删除，2替换，3插值
print(len(df_clean))

df_clean = df_clean.reset_index()  # 重置索引号
print(len(df_clean))
# 通过~取反，选取不包含['塔楼', '板塔结合', '暂无数据', '板楼']的行
df_clean = df_clean[~df_clean['建成时间'].isin(['塔楼', '板塔结合', '暂无数据', '板楼'])]
for i in range(len(df_clean)):
    #构建年限
    buildyears = int(df_clean.iloc[i, 10][0:4])
    #大于正常值取中位数
    if buildyears > 2021:
        buildyears = 2013
    # 小于常规值取反
    elif buildyears <= 0:
        buildyears = abs(buildyears)

print(len(df_clean))

# 保留部分字段
df_clean = df_clean[['区域', '地段', '小区', '空间', '面积', '朝向', '装修', '楼层', '建成时间', '单价每平', '总价']]
# df_cleans = df_clean[1:10]
# print(df_clean)

df_out = pd.DataFrame(df_clean, columns=[
    '区域', '地段', '小区', '空间', '面积', '朝向', '装修', '楼层', '建成时间', '单价每平', '总价'
])
df_out.to_csv('cq_pre-owned_house2.csv', index=False, index_label=False)
# 写入MySQL中
conn = create_engine('mysql+mysqldb://root:000000@localhost:3306/keshihua?charset=utf8')
# index为索引号，index_label下标
df_out.to_sql(name='cq_pre-ownedHouse2', con=conn, if_exists='append', index=False, index_label=False)
