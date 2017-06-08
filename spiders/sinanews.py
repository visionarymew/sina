# -*- coding: utf-8 -*-
from sina.items import SinaItem
from scrapy.linkextractors import LinkExtractor

import scrapy
import os

#用linkectractor分析连接(注意LINKS提取)

class SinanewsSpider(scrapy.Spider):
    name = "sinanews"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://news.sina.com.cn/guide/']

    #分析主目录获取所有大小类的连接,然后进入分类循环抓取新闻
    #debug change[@attr] to /attr
    def parse(self, response):
        titlelist=response.xpath('//div[@id="tab01"]/div')
        dirroot ='d:/study/sina/'
        
        #分析每个大类获取子类信息
        for each in titlelist[:-1]:
            item = SinaItem()
            item['parentUrls'] = each.xpath('.//h3/a/@href').extract()[0]
            item['parentTitle'] = each.xpath('.//h3/a/text()').extract()[0]
            item['subUrls'] = each.xpath('.//ul/li/a/@href').extract()
            item['subTitle'] = each.xpath('.//ul/li/a/text()').extract()
            
            #按照小分类创建文件夹
            parentroot = dirroot + item['parentTitle'] + '/'
            subroot = [parentroot + x +'/' for x in item['subTitle'] ]

            #先确认主分类文件夹
            if not os.path.exists(parentroot):
                os.mkdir(parentroot)

            #创建子类文件，遍历整个子类的新闻
            for i in range(len(subroot)):
                if not os.path.exists(subroot[i]):
                    os.mkdir(subroot[i])
                item['savepath'] = subroot[i]

                yield scrapy.Request(url = item['subUrls'][i],meta={'item':item},callback=self.parsenext)

    #分析子类页面获得每个新闻连接
    def parsenext(self,response):
        item = response.meta['item']
        #抓取所有连接，连接以分区连接为开头，以shtml为结尾
        links = [x.url for x in  LinkExtractor(allow='.shtml').extract_links(response)]
        links = [x for x in links if x.startswith(tuple(item['subUrls']))]
        for url in links:
            yield scrapy.Request(url = url,meta={'item':item},callback=self.parsenews)

    #分析子类下的每个新闻页内容
    def parsenews(self,response):
        item = response.meta['item']
        newstitle = response.xpath("//meta[@property='og:title']/@content").extract()[0]
        textlines = response.xpath("//div[@id='artibody']//p/text()").extract()

        item['head'] = newstitle
        content = str('\n'.join(textlines)).replace('\u3000','')
        content = content.replace('\xa0','')
        item['content'] = content

        yield item
