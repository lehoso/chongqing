import random

import pandas as pd
import matplotlib  # 导入图表模块
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from sklearn.metrics.pairwise import linear_kernel
import matplotlib.pyplot as plt  # 图像展示库


class recommendation:
    def get_cleanAndalgorithm(data):
        # 避免中文乱码
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei显示中文
        matplotlib.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符，使用rc配置文件来自定义
        # 简单清洗
        # data = pd.read_csv('cq_pre-owned_house2.csv')  # 读取csv数据
        data = pd.read_csv(data)  # 读取csv数据
        data = data.drop_duplicates(['小区'])
        data = data.reset_index(drop=True)

        # 使用sklearn库中的TfIdfVectorizer来计算TF-IDF矩阵
        """
        算法来源街及解释
        https://blog.csdn.net/Joenyye/article/details/80912909
        """
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(data['地段'])
        # print(tfidf_matrix.shape)#99个地段
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        indices = pd.Series(data.index, index=data['小区']).drop_duplicates()
        return data, cosine_sim, indices

    def get_recommendation(data, apartment, cosine_sim, indices):
        idx = indices[apartment]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:30]
        apartment_indices = [i[0] for i in sim_scores]
        return data['小区'].iloc[apartment_indices]

    # 是计算得到与XXX相似的小区，根据结果，推荐的相关小区几乎都属于同一地段
    # https://blog.csdn.net/Joenyye/article/details/80912909

    def exportImg(apartment):
        f = open("k.txt", "w", encoding='utf-8')
        for line in apartment:
            f.write(line + '\n')
        f.close()

        with open("k.txt", encoding="utf-8") as file:
            # 1.读取文本内容
            text = file.read()
            # 2.设置词云的背景颜色、宽高、字数
            wordcloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf",
                                  background_color="white", width=600,
                                  height=300, max_words=50).generate(text)
            # 3.生成图片
            image = wordcloud.to_image()
            # 4.显示图片
            plt.figure()
            plt.imshow(image)
            plt.axis('off')  # 关闭坐标轴
            plt.show()

    def tansfer(data):
        clean, cosine_sim, indices = recommendation.get_cleanAndalgorithm(data)
        ap = clean['小区'][random.randint(0, 1014)]
        apartment = recommendation.get_recommendation(clean, ap, cosine_sim, indices)
        recommendation.exportImg(apartment)

# if __name__ == '__main__':
#     apartment = get_recommendation(data['小区'][random.randint(0, 1014)])
#     print(apartment)
#     exportImg(apartment)

# if __name__ == '__main__':
#     data = 'cq_pre-owned_house2.csv'
#     # data, apartment, cosine_sim, indices
#     clean, cosine_sim, indices = recommendation.get_cleanAndalgorithm(data)
#     ap = clean['小区'][random.randint(0, 1014)]
#     apartment = recommendation.get_recommendation(clean, ap, cosine_sim, indices)
#     recommendation.exportImg(apartment)
