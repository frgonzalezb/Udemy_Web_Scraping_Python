# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import os
import sqlite3

# useful for handling different item types with a single interface
from scrapy_db.spiders.transcripts import TranscriptsSpider

import pymongo

from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    force=True,
    filename='./scrapy.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    encoding='utf-8'
)


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


class SQLitePipeline:

    def open_spider(self, spider: TranscriptsSpider) -> None:
        logging.info('PIPELINE — Spider opened!')
        self.connection = sqlite3.connect('scrapy.db')
        self.cursor = self.connection.cursor()
        query: str = 'CREATE TABLE IF NOT EXISTS transcripts ('\
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'\
            'title TEXT,'\
            'plot TEXT,'\
            'script TEXT,'\
            'url TEXT'\
            ')'
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError as error:
            logging.error('PIPELINE — Error creating table!')
            logging.error(error)

    def process_item(self, item: dict, spider: TranscriptsSpider) -> dict:
        query: str = 'INSERT INTO transcripts (title, plot, script, url) '\
            'VALUES (?, ?, ?, ?)'
        try:
            self.cursor.execute(
                query,
                (item['title'], item['plot'], item['script'], item['url'])
            )
            self.connection.commit()
        except sqlite3.OperationalError as error:
            logging.error('PIPELINE — Error inserting item!')
            logging.error(error)
        return item

    def close_spider(self, spider: TranscriptsSpider) -> None:
        logging.info('PIPELINE — Spider closed!')
        self.connection.close()
