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


URL: str = 'https://www.audible.com/search'


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


def run_script() -> None:
    options: Options = Options()
    # options.headless = True  # DEPRECADO!!
    # https://www.selenium.dev/blog/2023/headless-is-going-away/
    options.add_argument("--headless=new")

    driver: webdriver.Chrome = webdriver.Chrome(options=options)
    driver.get(URL)

    container: WebElement = driver.find_element(
        By.CLASS_NAME,
        'adbl-impression-container'
    )

    products: list[WebElement] = container.find_elements(
        By.XPATH,
        './/li[contains(@class, "productListItem")]'
    )

    book_titles: list[str] = []
    book_authors: list[str] = []
    book_runtimes: list[str] = []

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

        time.sleep(1)

    driver.quit()

    df: pd.DataFrame = pd.DataFrame({
        'Title': book_titles,
        'Author': book_authors,
        'Runtime': book_runtimes
    })

    print('\nDataframe created successfully!', '\n', df)

    base_dir: str = './06_Proyecto1_AudibleBot/res/'
    filename: str = 'books.csv'

    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    df.to_csv(base_dir + filename, index=False)
    print('\nThis script has finished its job successfully!')


if __name__ == '__main__':
    run_script()
