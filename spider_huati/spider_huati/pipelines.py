# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class SpiderHuatiPipeline(object):

    def __init__(self):
        pass

    def process_item(self,item,spider):
        # self.file = open('Data_huati_'+item['title']+'.json','ab+')
        # line=json.dumps(dict(item),ensure_ascii=False,indent=2) + "\n"
        # self.file.write(line)
        # self.file.close()
        # return item
        pass
