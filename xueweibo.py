# encoding:UTF-8
# 运行这个比较好
import pymysql,re,time,requests,urllib

from collections import OrderedDict


#weibo_id = input('输入单条微博ID：')
weibo_id = 4295689414745032

weibo_id = str(weibo_id)

# url='https://m.weibo.cn/single/rcList?format=cards&id=' + weibo_id + '&type=comment&hot=1&page={}' #爬热门评论

url='https://m.weibo.cn/api/comments/show?id=' + weibo_id + '&page={}' #爬时间排序评论

headers = {
    'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Host' : 'm.weibo.cn',
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Referer' : 'https://m.weibo.cn/status/' + weibo_id,
    'Cookie' : 'SINAGLOBAL=141.168.38.92_1504579374.881367; U_TRS1=000000cb.69a36db6.59ae3cf7.995ca55f; SCF=AqXGxNOquTe1mBczyPjLLkl8crKbd1l0W-1Xz-e9CEIudmY1ldTihAOqIjOOFvEnbZraRUDvgDpRxSxrz2cIOkE.; vjuids=2f05a67e4.161eeafbba4.0.c913c731f00fa; vjlast=1520127950.1520127950.30; lxlrttp=1530880371; UOR=,,; ULV=1537455180603:10:1:1:203.219.171.126_1536395176.31946:1534344199768; Apache=172.16.138.141_1539099515.157516; SUB=_2AkMs4ESkdcPxrAZQnPwQzW3naY5H-jyfNS1SAn7tJhMyAhgv7koLqSVutBF-XJbjK8SR5hbMhi_ysN-hzuIbqXSa; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhgXJP526jFjFAd38-.Ve4Y',
    'DNT' : '1',
    'Connection' : 'keep-alive',
    }

i = 0
comment_num = 1
while True:
    r = requests.get(url = url.format(i),headers = headers)
    comment_page = r.json()['data']['data']
    if r.status_code ==200:
        try:
            print('正在读取第 %s 页评论：' % i)
            for j in range(0,10):
                print('正在读取第 %s 页评论：' % i + '第 %s 条评论' % comment_num)
                user = comment_page[j]
                comment_id = user['user']['id']
                print(comment_id)
                user_name = user['user']['screen_name']
                print(user_name)
                created_at = user['created_at']
                print(created_at)
                text = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]','',user['text'])
                print(text)
                likenum = user['like_counts']
                print(likenum)
                source = re.sub('[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]','',user['source'])
                print(source + '\r\n')

                # utf8mb4可以保存emoji
                # utf8是默认保存3字节
                # emoji是四个字节的
                conn = pymysql.connect(host='localhost',user='root',password='456852gg',charset="utf8",use_unicode = False)

                cur = conn.cursor()
                sql = "insert into nlp.love_guan(comment_id,user_name,created_at,text,likenum,source) values(%s,%s,%s,%s,%s,%s)"
                param = (comment_id,user_name,created_at,text,likenum,source)
                try:
                    A = cur.execute(sql,param)
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()
                comment_num+=1
            i+=1
            time.sleep(3)
        except:
            i+1
            pass
    else:
        continue






