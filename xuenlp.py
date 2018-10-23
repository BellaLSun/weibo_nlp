# encoding:UTF-8
import pymysql,re
import jieba
import jieba.posseg as pseg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from snownlp import SnowNLP
from wordcloud import WordCloud,ImageColorGenerator
from collections import Counter
from wordcloud import STOPWORDS

def readmysql(): #读取数据库
    commentlist = []
    textlist = []
    userlist = []
    conn =pymysql.connect(host='127.0.0.1', user='root', password='456852gg', charset="utf8")    #连接服务器
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM nlp.love_guan")
        rows = cur.fetchall()
        for row in rows:
            row = list(row)
            #del row[0]
            # 去重
            if row not in commentlist:
                commentlist.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                user_name = row[1]
                userlist.append(user_name)
                text = row[3]
                if text:
                    textlist.append(text)

    return commentlist,userlist,textlist


def wordtocloud(textlist):
    fulltext = ''
    isCN = 1
    backgroud_Image = plt.imread("bg.jpg")
    stopwords = STOPWORDS.copy()
    stopwords.add("小虫儿")
    cloud = WordCloud(font_path='font.ttf', # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
            background_color="white",  # 背景颜色
            max_words=50,  # 词云显示的最大词数
            mask=backgroud_Image,  # 设置背景图片
            max_font_size=100,  # 字体最大值
            stopwords=stopwords,
            random_state=42,
            width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
            )

    for li in textlist:
        fulltext += ' '.join(jieba.cut(li,cut_all = False))

    wc = cloud.generate(fulltext)
    plt.figure("颖宝结婚啦！")
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)
    wc.to_file('微博评论词云.png')



# 情感分析
def snowanalysis(textlist):
    sentimentslist = []
    for li in textlist:
        s = SnowNLP(li)
        # print(li)
        # print(s.sentiments)
        sentimentslist.append(s.sentiments)
    fig1 = plt.figure("sentiment")
    plt.hist(sentimentslist,bins=np.arange(0,1,0.1))
    plt.show()

# emoji表情玫瑰图
def emojilist(textlist):
    emojilist = []
    for li in textlist:
        emojis = re.findall(re.compile(u'(\[.*?\])',re.S),li)
        if emojis:
            for emoji in emojis:
                emojilist.append(emoji.replace('\n',''))

    v1 = (emojilist.count('5'))

    print("emojilist" + str(emojilist))



if __name__=='__main__':
    commentlist,userlist,textlist = readmysql()
    wordtocloud(textlist)
    snowanalysis(textlist)
    emojilist(textlist)

