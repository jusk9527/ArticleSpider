import MySQLdb
conn = MySQLdb.connect(host="45.76.219.234", user="root", passwd="password", db="article_spider", port=53306,
                            charset="utf8")
cursor = conn.cursor()
print(cursor)