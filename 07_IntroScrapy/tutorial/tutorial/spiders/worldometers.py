from typing import Any, Generator

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList, Selector


class WorldometersSpider(scrapy.Spider):
    name: str = "worldometers"
    allowed_domains: list[str] = ["www.worldometers.info"]
    start_urls: list[str] = [
        "https://www.worldometers.info/world-population/population-by-country"
    ]

    def parse(
            self,
            response: HtmlResponse
            ) -> Generator[scrapy.Request, Any, None]:
        # title: str | None = response.xpath('//h1/text()').get()
        countries: SelectorList[Selector] = response.xpath('//td/a')

        for country in countries:
            # name: str | None = country.xpath('.//text()').get()
            link: str | None = country.xpath('.//@href').get()

            # trabajando con links absolutos
            # abs_url: str = f'https://{self.allowed_domains[0]}{link}'
            # abs_url: str = response.urljoin(link)

            # trabajando con links relativos
            yield response.follow(url=link)
