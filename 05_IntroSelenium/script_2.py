"""
Script para hacer clic en un botón de la página de prueba.

Página web a usar, ofrecida por Frank:
https://www.adamchoi.co.uk/overs/detailed
"""


import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def click_element_by_xpath(url: str, xpath: str) -> None:
    """
    Simulates clicking on some element on the page, by using its XPath.
    """
    driver: webdriver.Chrome = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    driver.find_element(by=By.XPATH, value=xpath).click()
    time.sleep(3)
    select_dropdown_option(driver)
    time.sleep(3)
    extract_text_from_rows(driver)
    time.sleep(3)
    driver.quit()


def select_dropdown_option(driver: webdriver.Chrome) -> None:
    """
    Simulates clicking on a dropdown option.
    """
    dropdown: Select = Select(driver.find_element(by='id', value='country'))
    dropdown.select_by_visible_text('Spain')


def extract_text_from_rows(driver: webdriver.Chrome) -> None:
    """
    Extracts the text from the table rows.
    """
    rows = driver.find_elements(by=By.TAG_NAME, value='tr')
    for row in rows:
        print(row.text)  # dbg


if __name__ == '__main__':
    url: str = 'https://www.adamchoi.co.uk/overs/detailed'

    option: str = input('¿Absolute XPath or relative XPath? (1/2): ')
    if option == '1':
        xpath: str = '//*[@id="page-wrapper"]/div/home-away-selector/div/div/\
            div/div/label[2]'
        click_element_by_xpath(url, xpath)
    else:
        xpath: str = '//label[@analytics-event="All matches"]'
        click_element_by_xpath(url, xpath)
