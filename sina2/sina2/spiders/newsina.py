import os
import scrapy
from sina2.items import Sina2Item

class NewsinaSpider(scrapy.Spider):
    name = 'newsina'
    # 允许爬虫爬的域名
    allowed_domains = ['sina.com.cn']
    # 种子urls
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 需要进入网页源代码，找到需要的html element,可用 css or xpath
        # 通过某节点作为根结点进行大类链接遍历
        for each in response.xpath("//div[@id='tab01']/div[@data-sudaclick!='citynav']"):
            # 获取大类链接和大类标题
            majorUrl = each.xpath('./h3/a/@href').extract()[0].encode('utf-8')
            majorTitle = each.xpath('./h3/a/text()').extract()[0]

            # 设置大类储存路径
            majorPath = './data/' + majorTitle
            if not os.path.exists(majorPath):
                os.makedirs(majorPath)

            # 历遍小类链接
            for other in each.xpath("./ul/li/a"):
                # 获取以大类链接开头的小类链接
                if other.xpath('./@href').extract()[0].encode('utf-8').startswith(majorUrl):
                    # 注意item的位置，不同的位置会导致不同的结果。尽量不要把item的数据在外循环和内循环里面分别获取，如必须这样做，则创建空列表添加item来解决。
                    item = Sina2Item()
                    minorUrl = other.xpath('./@href').extract()[0].encode('utf-8')
                    minorTitle = other.xpath('./text()').extract()[0]
                    minorPath = majorPath + '/' + minorTitle
                    item['majorUrl'] = majorUrl
                    item['majorTitle'] = majorTitle
                    item['minorUrl'] = minorUrl
                    item['minorTitle'] = minorTitle
                    item['minorPath'] = minorPath

                if not os.path.exists(minorPath):
                    os.makedirs(minorPath)

                # 发送小类链接请求，使用meta参数把item数据传递到回调函数里面，通过response.meta['']得到数据
                yield scrapy.Request(url=item['minorUrl'].decode('utf-8'), meta={'meta_1':item}, callback=self.second_parse)

    def second_parse(self, response):
        # 获取meta参数里的‘meta1’ 的值，就是在上一个function的sub loop 里创建的item object
        meta_1 = response.meta['meta_1']
        items = []
        # 遍历小类里的子链接
        for each in response.xpath('//a/@href'):
            # 获取的子链接，以大类链接开头，以.shtml结尾
            if each.extract().encode('utf-8').startswith(meta_1['majorUrl']) and each.extract().endswith('.shtml'):
                item = Sina2Item()
                item['majorUrl'] = meta_1['majorUrl']
                item['majorTitle'] = meta_1['majorTitle']
                item['minorUrl'] = meta_1['minorUrl']
                item['minorTitle'] = meta_1['minorTitle']
                item['minorPath'] = meta_1['minorPath']
                item['subLink'] = each.extract().encode('utf-8')
                items.append(item)

        for each in items:
            # 发送子链接请求，使用meta参数把item数据传递到回调函数里面，通过response.meta['']得到数据
            yield scrapy.Request(url=each['subLink'].decode('utf-8'), meta={'meta_2':each}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']
        # 获取标题和内容不为空的子链接
        # if len(response.xpath("//h1[@class='main-title']/text()")) != 0 and len(response.xpath("//div[@class='article']/p/text()")) != 0:
        #   item['head'] = response.xpath("//h1[@class='main-title']/text()").extract()[0].encode('utf-8')
        #   item['content'] = ''.join(response.xpath("//div[@class='article']/p/text()").extract()).encode('utf-8')
        #   yield item
        item['head'] = response.xpath("//h1[@class='main-title']/text()")
        item['content'] = ''.join(response.xpath("//div[@id='artibody']/p/text()").extract())
        yield item
