# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
import pymongo
from scrapy.utils.project import get_project_settings

import scrapy
import os
from ArticleSpider import settings
import pymongo
class DouyuPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item




# 豆瓣top250下载
class DoubanspiderPipeline(object):
    def __init__(self):
        # 账号密码方式连接MongoDB | "mongodb://用户名:密码@公网ip:端口/"
        self.client = pymongo.MongoClient('mongodb://root:root@45.76.219.234:27017/')
        # 指定数据库
        self.db = self.client.test
        # 指定集合
        self.collection = self.db.douban

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.collection.insert(data)
        return item


# 斗鱼新秀主播图片下载
# class ImagesPipeline(ImagesPipeline):
#     # 获取下载setting里面的图片路径
#     IMAGES_STORE = get_project_settings().get("IMAGES_STORE")
#
#     # get_media_requests的作用就是为每一个图片链接生成一个Request对象，这个方法的输出将作为item_completed的输入中的results，results是一个元组，每个元组包括(success, imageinfoorfailure)。如果success=true，imageinfoor_failure是一个字典，包括url/path/checksum三个key。
#     def get_media_requests(self, item, info):
#         for i in item["imagesUrls"]:
#             image_url = i
#         yield scrapy.Request(image_url)
#
#     def item_completed(self, results, item, info):
#         # 固定写法，获取图片路径，同时判断这个路径是否正确，如果正确，就放到image_path里，ImagesPipline源码剖析可见
#         image_path = [x["path"] for ok, x in results if ok]
#         # 图片路径、名字
#         os.rename(self.IMAGES_STORE + "/" + image_path[0], self.IMAGES_STORE + "/" + item["name"] + ".jpg")
#         item["imagesPath"] = self.IMAGES_STORE + "/" + item["name"]
#
#         return item

# 斗鱼信息下载
class DouyuPipeline(object):
    def __init__(self):
        # 账号密码方式连接MongoDB | "mongodb://用户名:密码@公网ip:端口/"
        self.client = pymongo.MongoClient('mongodb://root:root@45.76.219.234:27017/')
        # 指定数据库
        self.db = self.client.test
        # 指定集合
        self.collection = self.db.douyu

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.collection.insert(data)
        return item


# 东莞阳光热线下载
class JsonWriterPipeline(object):

    def __init__(self):
        # 创建一个只写文件，指定文本编码格式为utf-8
        self.filename = codecs.open('sunwz.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(content)
        return item
    def spider_closed(self, spider):
        self.file.close()


import MySQLdb
# 博客园mysql入库
class MysqlPipeline(object):
    #采用同步的机制写入mysql, 比较慢
    def __init__(self):
        self.conn = MySQLdb.connect(host="45.76.219.234", user="root", passwd="password", db="article_spider", port=53306,
                            charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobblole_article(title, url, url_object_id,tags,content,create_date)
            VALUES (%s, %s, %s, %s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"],item["tags"],item["content"],item["create_date"]))
        self.conn.commit()


from twisted.enterprise import adbapi
class MysqlTwistedPipline(object):
    # 采用异步入库的机制写入mysql,比较快
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port=settings["MYSQL_PORT"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure  , item, spider):
        #处理异步插入的异常
        print (failure)

    # def do_insert(self, cursor, item):
    #     #执行具体的插入
    #     #根据不同的item 构建不同的sql语句并插入到mysql中
    #
    #     # 这里注意顺序啊，params加入的顺序要与sql语句协调一致阿！
    #
    #     insert_sql = """
    #         insert into jobblole_article(title, url, url_object_id,tags,content,create_date,front_image_path)
    #         VALUES (%s, %s, %s, %s,%s,%s,%s)
    #     """
    #
    #     params = list()
    #     params.append(item.get("title", ""))
    #     params.append(item.get("url", ""))
    #     params.append(item.get("url_object_id", ""))
    #     # front_image = ",".join(item.get("front_image_url", []))
    #     # params.append(front_image)
    #     params.append(item.get("tags", ""))
    #     params.append(item.get("content", ""))
    #     params.append(item.get("create_date", "1970-03-08"))
    #     params.append(item.get("front_image_path", ""))
    #
    #
    #     # insert_sql, params = item.get_insert_sql()
    #     cursor.execute(insert_sql, params)


    # 这里将sql语句及其参数写在item中比较好！减少冗余
    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

# 博客园图片们下载
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            print("没有图片")
        item['front_image_path'] = image_paths
        return item

    # def item_completed(self, results, item, info):
    #     if "front_image_url" in item:
    #         for ok, value in results:
    #             image_file_path = value["path"]
    #         item["front_image_path"] = image_file_path
    #
    #     return item


from ArticleSpider.items import JobBoleArticleItem
class ElasticsearchPipeline(object):
    # 将数据写入到es中

    def process_item(self, item, spider):
        # 将item转换为es的数据
        item.save_to_es()
        return item
















