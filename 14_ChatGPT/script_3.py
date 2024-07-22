"""
Generado con ChatGPT-4o.
Ligeras adaptaciones por frgonzalezb.
"""


import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv  # no estaba originalmente, pero importa


load_dotenv()

# Path to your ChromeDriver
chrome_driver_path = os.environ['DRIVER_PATH']

# Set up Chrome options (no headless mode)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the page
url = 'https://x.com/biobio'

# Open the URL
driver.get(url)

# Scroll down to load more content and extract elements
last_height = driver.execute_script("return document.body.scrollHeight")
results = []
while True:
    # Locate elements by XPath
    elements = driver.find_elements(By.XPATH, '//div[@lang]')

    # Extract and print text from each element
    for element in elements:
        text = element.text
        if text not in results:  # Avoid duplicates
            results.append(text)
            print(text)
            time.sleep(15)  # Wait 15 seconds between each extraction

    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the new content
    time.sleep(15)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Close the WebDriver
driver.quit()

# Print all the results as a list
print(results)
