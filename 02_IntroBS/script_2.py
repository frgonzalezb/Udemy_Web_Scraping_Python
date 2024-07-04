from bs4 import BeautifulSoup
import requests


url: str = 'https://subslikescript.com/movie/Titanic-120338'
page: requests.Response = requests.get(url)
content: str = page.text
parser: str = 'lxml'

soup: BeautifulSoup = BeautifulSoup(content, parser)
print(soup.prettify())
