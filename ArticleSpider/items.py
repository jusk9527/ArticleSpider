import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from ArticleSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT



class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass




# 豆瓣top250
class DoubanspiderItem(scrapy.Item):
    # 电影标题
    title = scrapy.Field()
    # 电影评分
    score = scrapy.Field()
    # 电影信息
    content = scrapy.Field()
    # 简介
    info = scrapy.Field()



# 斗鱼星秀图片
class DouyuItem(scrapy.Item):
    room_id = scrapy.Field() # 房间号
    room_name = scrapy.Field() # 房间名
    game_name = scrapy.Field()  # 类别
    name = scrapy.Field()  # 存储照片的名字
    imagesUrls = scrapy.Field()  # 照片的url路径
    imagesPath = scrapy.Field()  # 照片保存在本地的路径
    imagesYunPath = scrapy.Field()  # 存储在云端的路径，暂且没用
    anchor_city = scrapy.Field()  # 地点


# 阳光热线问政平台
class wzSunItem(scrapy.Item):
    # 每个帖子标题
    title = scrapy.Field()
    # 每个帖子的编号
    number = scrapy.Field()
    # 每个帖子的文字内容
    content = scrapy.Field()
    # 每个帖子的url
    url = scrapy.Field()


from scrapy.loader.processors import MapCompose
from ArticleSpider.models.es_types import ArticleType
from w3lib.html import remove_tags
from elasticsearch_dsl.connections import connections
es = connections.create_connection(ArticleType._doc_type.using)
def add_jobble(value):
    return value+"啊哈哈"

def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
            used_words = used_words | new_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
            used_words.update(new_words)

    return suggests




# 博客园下载
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # 这种适用于itemload
        # input_processor = MapCompose(add_jobble)
    )
    create_date = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()


    def save_to_es(self):
        # 将item转换为es的数据
        article = ArticleType()

        article.title = self["title"]
        article.create_date = self["create_date"]
        article.url = self["url"]
        article.content = self["content"]

        article.meta.id = self["url_object_id"]
        article.front_image_url = self["front_image_url"]

        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.tags = self["tags"]

        article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        article.save()

        return


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()



def remove_splash(value):
    #去掉工作城市的斜线
    return value.replace("/","")


from w3lib.html import remove_tags

def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)

# 拉钩网职位信息
class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )

    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )

    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )

    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(input_processor=Join(","))
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url,
            tags, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"],
            self["work_years"], self["degree_need"], self["job_type"],
            self["publish_time"], self["job_advantage"], self["job_desc"],
            self["job_addr"], self["company_name"], self["company_url"],
            self["job_addr"], self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params






# 伯乐在线
class JobbolespiderItem(scrapy.Item):
    # 文章标题
    title = scrapy.Field()
    # 文章类别
    category = scrapy.Field()
    # 文章时间信息
    datatime = scrapy.Field()
    # 文章类容
    content = scrapy.Field()




# 妹子网
class MzituItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 文时间信息
    datatime = scrapy.Field()
    # 图片url 链接
    front_image_url = scrapy.Field()

    # url 链接
    base_url = scrapy.Field()

    # 图片数量
    max_images = scrapy.Field()



