from typing import Any, Generator, Literal

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name: Literal['transcripts'] = "transcripts"
    allowed_domains: list[str] = ["subslikescript.com"]
    start_urls: list[str] = ["https://subslikescript.com/movies_letter-X"]

    script_xpath: str = '//ul[contains(@class, "scripts-list")]/li/a'
    next_page_xpath: str = '(//a[contains(@rel, "next")])[1]'
    rules: tuple[Rule] = (
        Rule(
            LinkExtractor(restrict_xpaths=script_xpath),
            callback="parse_item",
            follow=True
        ),
        Rule(
            LinkExtractor(restrict_xpaths=next_page_xpath)
        ),
    )

    custom_settings: dict[str, Any] = {
        'DOWNLOAD_DELAY': 0.5,  # Fija un retraso de 0.5 segundos
    }

    def parse_item(self, response: HtmlResponse):
        article_xpath: str = '//article[contains(@class, "main-article")]'
        article: SelectorList[Selector] = response.xpath(article_xpath)
        yield {
            'title': article.xpath('./h1/text()').get(),
            'plot': article.xpath('./p').get() if article.xpath('./p') else '',
            # 'script': article.xpath('./div[@class="full-script"]').getall(),
            'url': response.url
        }
