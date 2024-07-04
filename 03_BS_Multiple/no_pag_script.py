"""
Script adaptado para web scraping de múltiples links (sin paginación).

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


def scrap_the_shit_out_of_it(url: str) -> BeautifulSoup:
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


root: str = 'https://subslikescript.com'
url: str = f'{root}/movies/'
soup = scrap_the_shit_out_of_it(url)
box = soup.find('article', class_='main-article')

links: list[str] = []
for link in box.find_all('a', href=True):
    links.append(link['href'])

for link in links:
    time.sleep(1)
    soup = scrap_the_shit_out_of_it(f'{root}{link}')
    box = soup.find('article', class_='main-article')  # coincidencia

    title: str = box.find('h1').getText()
    transcript: str = box.find('div', class_='full-script').getText(' ', True)

    filename: str = f'./03_BS_Multiple/res/{sanitize_filename(title)}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(title.upper() + '\n\n' + transcript + '\n\n' * 2)
