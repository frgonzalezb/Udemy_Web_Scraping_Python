# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyDbPipeline:

    def open_spider(self, spider):
        logging.warning('PIPELINE — Spider opened!')

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        logging.warning('PIPELINE — Spider closed!')
