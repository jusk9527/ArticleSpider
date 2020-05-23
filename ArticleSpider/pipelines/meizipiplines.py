import pymongo

# Meizi网下载爬虫
class MeiziPipeline(object):
    def __init__(self):
        # 账号密码方式连接MongoDB | "mongodb://用户名:密码@公网ip:端口/"
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        # 指定数据库
        self.db = self.client.meizi
        # 指定集合
        self.collection = self.db.meizi

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.collection.insert(data)




import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item