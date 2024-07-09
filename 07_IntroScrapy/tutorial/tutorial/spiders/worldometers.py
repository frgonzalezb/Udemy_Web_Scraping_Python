from typing import Any, Generator

import scrapy
from scrapy.http.response.html import HtmlResponse


class WorldometersSpider(scrapy.Spider):
    name: str = "worldometers"
    allowed_domains: list[str] = ["www.worldometers.info"]
    start_urls: list[str] = [
        "https://www.worldometers.info/world-population/population-by-country"
    ]

    def parse(
            self,
            response: HtmlResponse
            ) -> Generator[dict[str, Any], Any, None]:
        title: str | None = response.xpath('//h1/text()').get()
        countries: list[str] = response.xpath('//td/a/text()').getall()

        yield {
            'title': title,
            'countries': countries,
        }
