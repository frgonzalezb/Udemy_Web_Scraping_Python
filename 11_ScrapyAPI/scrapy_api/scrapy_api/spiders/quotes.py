import json
import logging
from typing import Any, Generator

import scrapy
from scrapy.http.response.html import HtmlResponse


logging.basicConfig(
    filename='./quotes.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    encoding='utf-8'
)


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    custom_settings: dict[str, Any] = {
        'DOWNLOAD_DELAY': 0.5,  # Fija un retraso de 0.5 segundos
    }

    def parse(
            self,
            response: HtmlResponse
            ) -> Generator[dict[str, Any], Any, None]:

        json_response: Any = json.loads(response.body)
        quotes: Any = json_response.get('quotes')

        for quote in quotes:
            yield {
                'author': quote.get('author').get('name'),
                'tags': quote.get('tags'),
                'quotes': quote.get('text'),
            }

        has_next: Any = json_response.get('has_next')
        if has_next:
            next_page: Any = json_response.get('page') + 1
            yield response.follow(
                url=f'https://quotes.toscrape.com/api/quotes?page={next_page}',
                callback=self.parse
            )
