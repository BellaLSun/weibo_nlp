
ip address中:  4279910752960721
How to get cookies:
https://www.jianshu.com/p/f603e922c455
mysql password: https://blog.csdn.net/pariese/article/details/77527813


##
reference
利用500W条微博语料对评论进行情感分析
https://zhuanlan.zhihu.com/p/30061051
#
Python采集微博热评进行情感分析
https://juejin.im/post/5a55e558518825732646b325
#
MySQL之终端(Terminal)管理MySQL
https://www.cnblogs.com/GarveyCalvin/p/4297221.html
https://www.jianshu.com/p/0ac446272dad

# terminal
$ sudo /Library/StartupItems/MySQLCOM/MySQLCOM start
## create database
create database 
default character set: utf8 ; default collation: utf8_unicode_ci
'''
CREATE DATABASE nlp;
USE nlp;

CREATE TABLE love_guan(
comment_id longtext,
user_name VARCHAR (255),
created_at VARCHAR (255),
text longtext,
likenum INT (11),
source VARCHAR (255)
);
'''
