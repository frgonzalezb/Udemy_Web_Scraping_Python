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
        """
        Parses the HTML response from the population-by-country URL.
        """
        # title: str | None = response.xpath('//h1/text()').get()
        countries: SelectorList[Selector] = response.xpath('//td/a')

        for country in countries:
            name: str | None = country.xpath('.//text()').get()
            link: str | None = country.xpath('.//@href').get()

            # trabajando con links absolutos
            # abs_url: str = f'https://{self.allowed_domains[0]}{link}'
            # abs_url: str = response.urljoin(link)

            # trabajando con links relativos
            yield response.follow(
                url=link,
                callback=self.parse_country,
                meta={'country': name}
            )

    def parse_country(
            self,
            response: HtmlResponse
            ) -> Generator[dict[str, str | None], Any, None]:
        """
        Parses the HTML response from each country population URL.
        """
        country = response.request.meta['country']
        xpath: str = '(//table[contains(@class, "table")])[1]/tbody/tr'
        rows: SelectorList[Selector] = response.xpath(xpath)

        for row in rows:
            year: str | None = row.xpath('.//td[1]/text()').get()
            population: str | None = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country': country,
                'year': year,
                'population': population
            }
