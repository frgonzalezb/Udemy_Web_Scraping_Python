"""
Script adaptado para web scraping de múltiples links (con paginación).

-------------------------------------------------
NOTA DE FRANK ANDRADE:

Actualización 2024: El sitio web que estamos scrapeando no permite
múltiples solicitudes en un corto período de tiempo, por lo que es
posible que veas un error después de extraer 9/10 elementos. Podemos
solucionar esto fácilmente agregando una espera de 1 segundo en el
código:

from bs4 import BeautifulSoup
import requests
import time

# mismo código

# Extrayendo los transcripts
for link in links:
    time.sleep(1)
"""


from bs4 import BeautifulSoup
import requests
import time
import re
import os


def scrap_all_the_shit_out_of_it(url: str) -> BeautifulSoup:
    """
    Mucho código repetido en el script original de Frank.
    Así que decidí mejor crear una función. :P
    """
    page: requests.Response = requests.get(url)
    content: str = page.text
    parser: str = 'lxml'

    return BeautifulSoup(content, parser)


def sanitize_filename(filename) -> str:
    """
    Función no contemplada en el script original de Frank.

    Modifica ligeramente el nombre de un título obtenido del scraping,
    en caso de que el nombre de un título posea caracteres prohibidos en
    Windows (por ejemplo, los signos de interrogación), a fin de evitar
    OSError.
    """
    forbidden_chars = r'[<>:"/\\|?*]'
    sanitized_filename = re.sub(forbidden_chars, '-', filename)
    return sanitized_filename


def create_file(title: str, transcript: str) -> None:
    """
    Función utilitaria para crear los archivos de salida y clarificar
    el código un poco. :P
    """
    base_dir: str = './03_BS_Multiple/res/movies_letter-A/'
    filename: str = f'{sanitize_filename(title)}.txt'

    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    with open(base_dir + filename, 'w', encoding='utf-8') as f:
        f.write(title.upper() + '\n\n' + transcript + '\n\n' * 2)


root: str = 'https://subslikescript.com'
url: str = f'{root}//movies_letter-A'
soup: BeautifulSoup = scrap_all_the_shit_out_of_it(url)

pagination = soup.find('ul', class_='pagination')  # THIS!
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text
url_param: str = '?page='

links: list[str] = []
for page in range(1, int(last_page) + 1)[:2]:  # solo 2 primeras páginas
    page_params = url_param + str(page)
    soup: BeautifulSoup = scrap_all_the_shit_out_of_it(url + page_params)

    box = soup.find('article', class_='main-article')

    for link in box.find_all('a', href=True):
        links.append(link['href'])

    for link in links:
        try:
            time.sleep(1)
            print(f'\t{link=}')  # dbg
            soup: BeautifulSoup = scrap_all_the_shit_out_of_it(f'{root}{link}')
            box = soup.find('article', class_='main-article')  # coincidencia

            title: str = box.find('h1').getText()
            transcript: str = box.find(
                'div', class_='full-script'
            ).getText(' ', True)

            create_file(title, transcript)

        except Exception as e:
            print(f'\tERROR: The link "{link}" is not working because of {e}')

        except KeyboardInterrupt:
            exit()
