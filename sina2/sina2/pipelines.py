# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Sina2Pipeline:
    def process_item(self, item, spider):
        # 设置保存的文件名，把子链接去掉'http://'和'.shtml'，把'/'替换成‘_’，保存为txt文件格式
        self.filename = item['subLink'].decode('utf-8')[7:-6].replace('/', '_') + '.txt'
        self.file = open(item['minorPath'] + '/' + self.filename, 'w')
        self.file.write(item['subLink'].decode('utf-8') + '\n' + item['content'])
        self.file.close()
        return item
