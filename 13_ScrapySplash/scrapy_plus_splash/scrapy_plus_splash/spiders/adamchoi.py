import logging
from typing import Any, Generator

import scrapy
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
    allowed_domains = ["www.adamchoi.co.uk"]
    # start_urls = ["https://www.adamchoi.co.uk"]

    script: str = '''
        function main(splash, args)
            splash.private_mode_enabled = false

            assert(splash:go(args.url))
            assert(splash:wait(3))

            all_matches = splash:select_all("label.btn.btn-sm.btn-primary.ng-pristine.ng-untouched.ng-valid.ng-not-empty")
            all_matches[2]:mouse_click()
            assert(splash:wait(3))
            splash:set_viewport_full()

            return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
            }
        end
    '''

    custom_settings: dict[str, Any] = {
        'DOWNLOAD_DELAY': 0.5,  # Fija un retraso de 0.5 segundos
    }

    def start_requests(self) -> Generator[SplashRequest, Any, None]:
        url: str = 'https://www.adamchoi.co.uk/overs/detailed'
        yield SplashRequest(
            url=url,
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': self.script, 'url': url},
        )

    def parse(self, response) -> None:
        logging.debug(f'{response.body=}')
