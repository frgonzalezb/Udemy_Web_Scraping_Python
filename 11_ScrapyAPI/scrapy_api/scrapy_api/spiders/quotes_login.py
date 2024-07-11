import os
import logging
from typing import Any, Generator

from dotenv import load_dotenv

import scrapy
from scrapy import FormRequest
from scrapy.http.response.html import HtmlResponse


load_dotenv()


logging.basicConfig(
    filename='./quotes.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
    encoding='utf-8'
)


class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    custom_settings: dict[str, Any] = {
        'DOWNLOAD_DELAY': 0.5,  # Fija un retraso de 0.5 segundos
    }

    def parse(
            self,
            response: HtmlResponse
            ) -> Generator[FormRequest, Any, None]:

        csrf_token: str | None = response.xpath(
            '//input[@name="csrf_token"]/@value'
        ).get()
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': os.environ['USERNAME'],
                'password': os.environ['PASSWORD']
            },
            callback=self.check_login
        )

    def check_login(self, response: HtmlResponse) -> None:
        if response.xpath('//a[@href="/logout"]').get():
            logging.info('Login successful!')
