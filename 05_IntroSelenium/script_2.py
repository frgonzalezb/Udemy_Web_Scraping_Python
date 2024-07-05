"""
Script para hacer clic en un botón de la página de prueba.

Página web a usar, ofrecida por Frank:
https://www.adamchoi.co.uk/overs/detailed
"""


import time
from selenium import webdriver


def click_element_by_xpath(url: str, xpath: str) -> None:
    """
    Simulates clicking on some element on the page, by using its XPath.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    driver.find_element(by='xpath', value=xpath).click()
    time.sleep(3)
    driver.quit()


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
