"""
Proyecto 1: Audible Bot

Página a usar: https://www.audible.com/search
"""


import os
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement  # 4 typing
from selenium.common.exceptions import NoSuchElementException


def get_driver() -> webdriver.Chrome:
    options: Options = Options()
    # options.headless = True  # DEPRECADO!!
    # https://www.selenium.dev/blog/2023/headless-is-going-away/
    options.add_argument("--headless=new")

    driver: webdriver.Chrome = webdriver.Chrome(options=options)
    return driver


def get_element_as_text(
        web_element: WebElement,
        tag: str,
        class_name: str
        ) -> str:
    """
    Extracts the text from an element, if any.
    """
    selector: str = f'.//{tag}[contains(@class, "{class_name}")]'
    try:
        return web_element.find_element(By.XPATH, selector).text
    except NoSuchElementException:
        return f'WARNING: {class_name} element not found.'


def create_csv_file(data: tuple[list[str]]) -> None:
    """
    Creates a CSV file with the extracted data.
    """
    df: pd.DataFrame = pd.DataFrame({
        'Title': data[0],
        'Author': data[1],
        'Runtime': data[2]
    })

    print('\nDataframe created successfully!', '\n', df)

    base_dir: str = './06_Proyecto1_AudibleBot/res/'
    filename: str = 'books.csv'

    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    df.to_csv(base_dir + filename, index=False)


def run_script() -> None:
    url: str = 'https://www.audible.com/es_US/search'

    driver = get_driver()
    driver.get(url)

    pagination: WebElement = driver.find_element(
        By.XPATH,
        './/ul[contains(@class, "pagingElements")]'
    )
    pages: list[WebElement] = pagination.find_elements(By.TAG_NAME, 'li')
    last_page: int = int(pages[-2].text)

    book_titles: list[str] = []
    book_authors: list[str] = []
    book_runtimes: list[str] = []

    """
    NOTA PARA MI YO DEL FUTURO: El modo de Frank ya no funciona y he
    decidido hacerlo como en el script de BeautifulSoup, mediante el uso
    de params. Dejaré el estilo de Frank comentado más abajo.
    """

    current_page: int = 1
    params: str = f'?page={current_page}'
    for page in range(1, last_page + 1)[:2]:  # solo 2 primeras páginas
        print(f'\nCurrent page: {page}/{last_page}')
        driver.get(url + params)

        container: WebElement = driver.find_element(
            By.CLASS_NAME,
            'adbl-impression-container'
        )

        products: list[WebElement] = container.find_elements(
            By.XPATH,
            './/li[contains(@class, "productListItem")]'
        )

        for product in products:
            title: str = get_element_as_text(product, 'h3', 'bc-heading')
            book_titles.append(title)

            author: str = get_element_as_text(product, 'li', 'authorLabel')
            author = author.split('De: ')[-1]
            book_authors.append(author)

            runtime: str = get_element_as_text(product, 'li', 'runtimeLabel')
            runtime = runtime.split('Duración: ')[-1]
            book_runtimes.append(runtime)

            print(f'\n\t{title=}, \n\t{author=}, \n\t{runtime=}')  # dbg

            time.sleep(2)

        current_page += 1
        params = f'?page={current_page}'

    # while current_page <= last_page:
    #     print(f'\nCurrent page: {current_page}/{last_page}')

    #     for product in products:
    #         title: str = get_element_as_text(product, 'h3', 'bc-heading')
    #         book_titles.append(title)

    #         author: str = get_element_as_text(product, 'li', 'authorLabel')
    #         author = author.split('De: ')[-1]
    #         book_authors.append(author)

    #         runtime: str = get_element_as_text(product, 'li', 'runtimeLabel')
    #         runtime = runtime.split('Duración: ')[-1]
    #         book_runtimes.append(runtime)

    #         print(f'\n\t{title=}, \n\t{author=}, \n\t{runtime=}')  # dbg

    #         time.sleep(1)

    #     try:
    #         next_page: WebElement = driver.find_element(
    #             By.XPATH,
    #             './/span[contains(@class, "nextButton")]'
    #         )
    #         next_page.click()
    #     except NoSuchElementException:
    #         print('Last page reached!')
    #         break

    #     current_page += 1
    #     time.sleep(3)

    driver.quit()

    create_csv_file((book_titles, book_authors, book_runtimes))

    print('\nThis script has finished its job successfully!')


if __name__ == '__main__':
    run_script()
