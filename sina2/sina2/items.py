# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Sina2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 大类新闻链接，如新闻、体育等
    majorUrl = scrapy.Field()
    majorTitle = scrapy.Field()

    # 小类新闻链接，如新闻下面的国内
    minorUrl = scrapy.Field()
    minorTitle = scrapy.Field()
    # 小类存储路径
    minorPath = scrapy.Field()

    # 子链接
    subLink = scrapy.Field()
    # 子链接里面的标题和内容
    head = scrapy.Field()
    content = scrapy.Field()
