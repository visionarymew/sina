# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# cd d:/study/sina/sina


import os
import re

class SinaPipeline(object):

    def process_item(self, item, spider):
        thename = re.findall('[\w\u4e00-\u9fa5]*',item['head'])

        filename = ''.join(thename)+'.txt'


        with open(item['savepath'] + filename,'w') as f:
            f.write(item['content'])
            f.close()
        return item
