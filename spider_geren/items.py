# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderHuatiItem(scrapy.Item):
    #个人信息
    user_id = scrapy.Field()        #用户的id
    containerid = scrapy.Field()    #不知道
    name = scrapy.Field()           #用户的昵称
    sex = scrapy.Field()            #用户性别
    position = scrapy.Field()       #用户的位置
    introduction = scrapy.Field()   #用户简介
    birthday = scrapy.Field()       #生日
    email = scrapy.Field()         
    qq =scrapy.Field()
    blog = scrapy.Field()
    msn = scrapy.Field()
    company = scrapy.Field()
    university = scrapy.Field()
    #关注人信息
    fellows_id = scrapy.Field()         #该用户关注的用户的id
    fellows_name = scrapy.Field()       #该用户关注的用户的昵称
    fellows_image_url = scrapy.Field()
    #粉丝信息
    fans_id = scrapy.Field()
    fans_name = scrapy.Field()
    fans_image_url = scrapy.Field()
    #weibo信息
    weibo_id = scrapy.Field()                       #某条微博的id
    weibo_text = scrapy.Field()                     #某条微博的内容
    weibo_post_id = scrapy.Field()                  #发送该条微博的用户id
    weibo_post_name = scrapy.Field()                #发送该条微博的用户昵称
    weibo_original_poster_id = scrapy.Field()       #该条微博原创者id
    weibo_original_poster_name = scrapy.Field()     #该条微博原创者昵称
    weibo_original_text = scrapy.Field()
    weibo_repost_count = scrapy.Field()
    weibo_comments_count = scrapy.Field()
    weibo_attitudes_count = scrapy.Field()
    weibo_pics = scrapy.Field()
    weibo_is_original = scrapy.Field()              #该条微博是否为该博主始发
    #微博的评论信息
    comment_id = scrapy.Field()             #某条评论的id
    comment_from_id = scrapy.Field()        #该评论来自的博主的id
    comment_from_name = scrapy.Field()      #该评论来自的博主的昵称
    comment_text = scrapy.Field()           #该条评论的具体内容
    comment_from_profile_image_url = scrapy.Field()
    #微博转发信息
    repost_id = scrapy.Field()
    repost_from_id = scrapy.Field()
    repost_from_name = scrapy.Field()
    repost_text = scrapy.Field() 
    repost_from_profile_image_url = scrapy.Field()
    #点赞信息
    like_from_id = scrapy.Field()
    like_from_name = scrapy.Field()
    like_from_profile_image_url = scrapy.Field()
    like_for_weibo_id = scrapy.Field()



