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

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the Amazon page
url = (
    'https://www.amazon.com/s?k=self+help+books&crid=6TKLUINN59HH'
    '&sprefix=self+help%2Caps%2C222&ref=nb_sb_ss_ts-doa-p_1_9'
)

# Open the URL
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust if necessary

# Locate elements by XPath
elements = driver.find_elements(
    By.XPATH,
    '//span[@class="a-size-base-plus a-color-base a-text-normal"]'
)

# Extract and print text from each element
results = []
for element in elements:
    results.append(element.text)
    print(element.text)
    time.sleep(5)  # Wait 5 seconds between each extraction

# Close the WebDriver
driver.quit()

# Print all the results as a list
print(results)
