import os
import logging
from typing import Any, Generator

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList, Selector

from scrapy_splash import SplashRequest


logging.basicConfig(
    filename='./adamchoi.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    encoding='utf-8'
)


class AdamchoiSpider(scrapy.Spider):
    name = "adamchoi"
    # allowed_domains = ["www.adamchoi.co.uk"]
    # start_urls = ["https://www.adamchoi.co.uk"]

    custom_settings: dict[str, Any] = {
        'DOWNLOAD_DELAY': 0.5,  # Fija un retraso de 0.5 segundos
    }

    def get_lua_script(self) -> str:
        cwd: str = os.getcwd().replace('\\', '/')
        if cwd.endswith('scrapy_plus_splash'):
            cwd = cwd[: -len('scrapy_plus_splash')]
        with open(cwd + '/script.lua') as f:
            script: str = f.read()

        return script

    def start_requests(self) -> Generator[SplashRequest, Any, None]:
        script: str = self.get_lua_script()
        url: str = 'https://www.adamchoi.co.uk/overs/detailed'
        yield SplashRequest(
            url=url,
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': script, 'url': url},
        )

    def parse(
            self,
            response: HtmlResponse
            ) -> Generator[dict[str, str | None], Any, None]:

        logging.debug(f'{response.body=}')  # dbg
        rows: SelectorList[Selector] = response.xpath('//tr')

        for row in rows:
            yield {
                'date': row.xpath('./td[1]/text()').get(),
                'home_team': row.xpath('./td[2]/text()').get(),
                'score': row.xpath('./td[3]/text()').get(),
                'away_team': row.xpath('./td[4]/text()').get(),
            }
