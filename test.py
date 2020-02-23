# 导入pymysql模块
import pymysql
# 连接database
conn = pymysql.connect(
    host="127.0.0.1",
    port=53306,
    user="root",
    password="password",
    database="test",
    charset="utf8")
# 得到一个可以执行SQL语句并且将结果作为字典返回的游标
# 获取一个光标
cursor = conn.cursor()
print(cursor)