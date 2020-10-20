# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy



class QizhaSpider(scrapy.Spider):
    name = 'qizha'
    allowed_domains = ['c.tieba.baidu.com']
    start_urls = ['http://c.tieba.baidu.com/f?kw=%E5%A4%B1%E4%BF%A1']

    def parse(self, response):
        #页面中帖子的url 地址
        url_list = response.css('.j_th_tit::attr(href)').extract()
        for url in url_list:
            # print(url)
            yield scrapy.Request(url=parse.urljoin(response.url,url), callback= self.parse_detail)

        next_url = response.css('.next.pagination-item::attr(href)').extract()[0]
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url,next_url),callback=self.parse)


    def parse_detail(self,response):
        #帖子的标题
        title = response.css('.core_title_txt.pull-left.text-overflow::text').extract()
        if title:
            #作者
            authors = response.css('.p_author_name.j_user_card::text').extract()
            #内容
            contents = response.css('.d_post_content.j_d_post_content').extract()
            #进一步处理了内容
            contents = self.get_content(contents)

            ##处理帖子发送时间和楼数
            bbs_sendtime_list,bbs_floor_list = self.get_send_time_and_floor(response)

            for i in range(len(authors)):
                from spider_project.items import TiebaItem
                tieba_item = TiebaItem()
                tieba_item['title'] = title[0]
                tieba_item['author'] = authors[i]
                tieba_item['content'] = contents[i]
                tieba_item['reply_time'] = bbs_sendtime_list[i]
                tieba_item['floor'] = bbs_floor_list[i]

                return tieba_item

    def get_content(self,contents):
        content_list = []
        for content in contents:
            reg = ';\">(.*)</div>'
            result = re.findall(reg,content)
            if result:
                content_list.append(result[0])

        return content_list

    def get_send_time_and_floor(self,response):
        bbs_send_time_and_floor_list = response.css('.post-tail-wrap span[class=tail-info]::text').extract()
        i = 0
        bbs_send_time_list = []
        bbs_floor_list = []

        for lz in bbs_send_time_and_floor_list:
            if lz == '来自':
                bbs_send_time_and_floor_list.remove(lz)

        for bbs_send_time_and_floor in bbs_send_time_and_floor_list:

            if i%2 ==1 :
                bbs_floor_list.append(bbs_send_time_and_floor)

            if i%2 ==0 :
                bbs_send_time_list.append(bbs_send_time_and_floor)

            i += 1

        return bbs_send_time_list,bbs_floor_list
