from bs4 import BeautifulSoup
import requests


url: str = 'https://subslikescript.com/movie/Titanic-120338'
page: requests.Response = requests.get(url)
content: str = page.text
parser: str = 'lxml'

soup: BeautifulSoup = BeautifulSoup(content, parser)
# print(soup.prettify())

box = soup.find('article', class_='main-article')
if box is None:
    exit()

title: str = box.find('h1').getText()
transcript: str = box.find('div', class_='full-script').getText(' ', True)

with open('./02_IntroBS/res/titanic_script.txt', 'w', encoding='utf-8') as f:
    f.write(title.upper() + '\n\n' + transcript)
