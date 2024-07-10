# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import os

# useful for handling different item types with a single interface
from scrapy_db.spiders.transcripts import TranscriptsSpider

import pymongo

from dotenv import load_dotenv


load_dotenv()


class MongoDbPipeline:
    collection_name = 'transcripts'

    def open_spider(self, spider: TranscriptsSpider) -> None:
        logging.info('PIPELINE — Spider opened!')
        self.client = pymongo.MongoClient(os.environ['DB_URI'])
        self.db = self.client['ScrapyDB']

    def process_item(self, item: dict, spider: TranscriptsSpider) -> dict:
        logging.info('PIPELINE — Processing item...')
        self.db[self.collection_name].insert_one(item)
        return item

    def close_spider(self, spider: TranscriptsSpider) -> None:
        logging.info('PIPELINE — Spider closed!')
        self.client.close()
