# encoding:UTF-8
import webbrowser
import pymysql,re,time
import requests
import sys

sys.setdefaultencoding('utf-8')

# 赵丽颖结婚
# https://m.weibo.cn/status/4295689414745032
# json: https://m.weibo.cn/api/comments/show?id=4295689414745032&page=1
weibo_id = 4295689414745032

# 动态加载
url='https://m.weibo.cn/api/comments/show?id=' + weibo_id + '&page={}'
# 请求网址，得到json文件信息
html = requests.get(url) # 获得网页源代码
print(html)
# print(html.json())

# json， so no need to regex， （dictionary）with slice is much easier
# json and dictionary 高度兼容

data = html.json()['data']['data'][0]['text']
print (data)


comment_num = 1

## 正式开始
ii = 0
comment_num = 1
while ii <=100:  # 页数
    print('第 %s 页' % ii)
    ii = ii + 1
    time.sleep(3)
    url = url='https://m.weibo.cn/api/comments/show?id=' + weibo_id + '&page={'+ii+'}'
    html = requests.get(url)
    try:
        for jj in range(len(html.json()['data']['data'])):
            print('第 %s 条评论' % comment_num)
            created_at = html.json()['data']['data'][jj]['created_at']
            comment_id = html.json()['data']['data'][jj]['id']
            text = html.json()['data']['data'][jj]['text']
            text = re.sub('回复.*?:', '', text)
            source = html.json()['data']['data'][jj]['source']
            source = re.sub('<.*?>|</a>', '', str(source))
            user_name = html.json()['data']['data'][jj]['user']['screen_name']

            print(created_at)
            print(comment_id)
            print(text)
            print(source)
            print(user_name)
            print('\n')
            # 写入数据库
            conn = pymysql.connect(host='127.0.0.1', user='root', password='456852gg', charset="utf8", use_unicode=False)
            cur = conn.cursor()
            sql = "insert into nlp.love_guan(comment_id,user_name,created_at,text,likenum,source) values(%s,%s,%s,%s,%s,%s)"
            param = (comment_id, user_name, created_at, text, source)
            try:
                A = cur.execute(sql, param)
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
            comment_num += 1

    except:
        None
else:
		break

