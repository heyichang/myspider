# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TiebaItem(scrapy.Item):
    # 帖子的标题
    title = scrapy.Field()
    # 帖子的作者
    author = scrapy.Field()
    # 帖子的内容
    content = scrapy.Field()
    # 帖子回复的时间
    reply_time = scrapy.Field()
    # 帖子所在的楼数
    floor = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into baidu_tieba(title,author,content,reply_time,floor)" \
                     "values (%s,%s,%s,%s,%s)"

        params = (self['title'],self['author'],self['content'],self['reply_time'],self['floor'])
        return insert_sql,params
