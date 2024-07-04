from bs4 import BeautifulSoup
import requests


url: str = 'https://www.worldometers.info/world-population/'
page: requests.Response = requests.get(url)
parser: str = 'lxml'
soup: BeautifulSoup = BeautifulSoup(page.text, parser)
element = soup.find('h1')
print(element.text)  # Current World Population
