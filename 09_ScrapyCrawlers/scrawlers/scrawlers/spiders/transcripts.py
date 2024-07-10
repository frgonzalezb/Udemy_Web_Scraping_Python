from typing import Any, Generator, Iterable, Literal

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name: Literal['transcripts'] = "transcripts"
    allowed_domains: list[str] = ["subslikescript.com"]
    # start_urls: list[str] = ["https://subslikescript.com/movies_letter-X"]

    # Para cambiar user-agent desde el script
    # NOTA PARA MI YO DEL FUTURO: Por alguna razón, el backslash genera
    # una tabulación extraña en consola, así que usé concatenación
    browsers: list[str] = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/126.0.0.0',
        'Safari/537.36'
    ]
    user_agent: str = ' '.join(browsers)

    script_xpath: str = '//ul[contains(@class, "scripts-list")]/li/a'
    next_page_xpath: str = '(//a[contains(@rel, "next")])[1]'
    rules: tuple[Rule] = (
        Rule(
            LinkExtractor(restrict_xpaths=script_xpath),
            callback="parse_item",
            follow=True,
            process_request='set_user_agent'
        ),
        Rule(
            LinkExtractor(restrict_xpaths=next_page_xpath),
            process_request='set_user_agent'
        ),
    )

    custom_settings: dict[str, Any] = {
        'DOWNLOAD_DELAY': 0.5,  # Fija un retraso de 0.5 segundos
    }

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield scrapy.Request(
            url='https://subslikescript.com/movies_letter-X',
            headers={'User-Agent': self.user_agent}
        )

    def set_user_agent(
            self,
            request: scrapy.Request,
            spider: CrawlSpider
            ) -> scrapy.Request:
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(
            self,
            response: HtmlResponse
            ) -> Generator[dict[str, Any], Any, None]:
        article_xpath: str = '//article[contains(@class, "main-article")]'
        article: SelectorList[Selector] = response.xpath(article_xpath)
        yield {
            'title': article.xpath('./h1/text()').get(),
            'plot': article.xpath('./p').get() if article.xpath('./p') else '',
            # 'script': article.xpath('./div[@class="full-script"]').getall(),
            'url': response.url,
            'user-agent': response.request.headers['User-Agent']
        }
