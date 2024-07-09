from typing import Any, Generator

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList, Selector


class AudibleSpider(scrapy.Spider):
    name: str = "audible"
    allowed_domains: list[str] = ["www.audible.com"]
    start_urls: list[str] = ["https://www.audible.com/es_US/search"]

    def parse(
            self,
            response: HtmlResponse
            ) -> Generator[dict[str, Any], Any, None]:
        """
        Parses the HTML response from the URL.
        """
        xpath: str = '//div[@class="adbl-impression-container "]\
            //li[contains(@class, "productListItem")]'
        product_container: SelectorList[Selector] = response.xpath(xpath)

        for product in product_container:
            title: str = product.xpath(
                './/h3[contains(@class, "bc-heading")]/a/text()'
            ).get()
            author: list[str] = product.xpath(
                './/li[contains(@class, "authorLabel")]/span/a/text()'
            ).getall()
            runtime: str = product.xpath(
                './/li[contains(@class, "runtimeLabel")]/span/text()'
            ).get()
            runtime = runtime.split('Duración: ')[-1]

            yield {
                'title': title,
                'author': author,
                'runtime': runtime
            }
