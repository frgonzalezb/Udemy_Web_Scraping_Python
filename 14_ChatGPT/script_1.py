"""
Generado con ChatGPT-4o.
Ligeras adaptaciones por frgonzalezb.
"""


import requests
from bs4 import BeautifulSoup


# URL of the webpage to scrape
url = 'https://subslikescript.com/movies'

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the <ul> element with class "scripts-list"
    ul_element = soup.find('ul', class_='scripts-list')

    if ul_element:
        # Find all <a> elements inside the <ul> element
        a_elements = ul_element.find_all('a')

        # Iterate through each <a> element and print the text attribute
        for a in a_elements:
            print(a.text)
    else:
        print('No <ul> element with class "scripts-list" found.')
else:
    print(
        f'Failed to retrieve the webpage. Status code: {response.status_code}'
    )
