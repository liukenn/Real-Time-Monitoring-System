# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderHuatiItem(scrapy.Item):

    #话题排行榜
    title = scrapy.Field()#话题title
    pic = scrapy.Field()#话题图像
    containerid = scrapy.Field()#微博编号
    text = scrapy.Field()#话题内容

    #话题微博细节
    bid = scrapy.Field()#微博入口
    ID = scrapy.Field()#用户ID
    name = scrapy.Field()#用户名字
    #pic = scrapy.Field()#用户头像
    #text = scrapy.Field()#微博内容
    weibo_id = scrapy.Field()#用于寻找评论转发点赞
    reposts_count = scrapy.Field()#转发量
    comments_count = scrapy.Field()#评论量
    attitudes_count = scrapy.Field()#点赞量

    #点赞
    what = scrapy.Field()#标明是点赞数据
    #ID = scrapy.Field()#点赞人id
    #name = scrapy.Field()#点赞人名字

    #转发
    #what = scrapy.Field()#标明是转发数据
    #ID = scrapy.Field()#转发人id
    #name = scrapy.Field()#转发人名字
    #text = scrapy.Field()#转发人内容

    #评论
    #what = scrapy.Field()#标明是评论数据
    #ID = scrapy.Field()#评论人id
    #name = scrapy.Field()#评论人名字
    #text = scrapy.Field()#评论人内容