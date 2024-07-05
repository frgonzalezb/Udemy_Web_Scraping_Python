"""
Página web a usar, ofrecida por Frank:
https://www.adamchoi.co.uk/overs/detailed


NOTA: De acuerdo a la documentación de Selenium, desde la versión 4.6 ya
no es necesario setear el path del driver (driver_path) para ejecutar el
script y, por ende, no es necesario el ChromeDriver para casos de uso
generales.

Sin embargo, he decidido dejar ambos modos, con y sin ChromeDriver,
de manera seleccionable.

Fuente: https://www.selenium.dev/documentation/webdriver/drivers/service/
"""


import os
import time

from selenium import webdriver
from dotenv import load_dotenv


load_dotenv()


def setup_the_old_way(url: str) -> None:
    """Método usando el chromedriver.exe"""
    driver_path: str = os.environ['DRIVER_PATH']
    service = webdriver.ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(5)
    driver.quit()


def setup_the_new_way(url: str) -> None:
    """Método que no necesita el chromedriver.exe"""
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    driver.quit()


# usage
if __name__ == '__main__':
    url: str = 'https://www.adamchoi.co.uk/overs/detailed'

    option: str = input('¿Usar chromedriver.exe o el navegador web? (1/2): ')
    if option == '1':
        setup_the_old_way(url)
    else:
        setup_the_new_way(url)
