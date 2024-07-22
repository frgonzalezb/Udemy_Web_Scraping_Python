# Prompts utilizados para los scripts de esta carpeta


## Script 1

```Text
Please web scrap the following page with Python and BeautifulSoup: https://subslikescript.com/movies

Locate the element with the HTML tag "ul" and class="scripts-list", then locate and extract all the elements with the HTML tag "a" you can found inside it. For each HTML element "a", get the text attribute and print them to console.
```


## Script 2

```Text
Please web scrap the following page with Python, Selenium and ChromeDriver: https://www.amazon.com/s?k=self+help+books&crid=6TKLUINN59HH&sprefix=self+help%2Caps%2C222&ref=nb_sb_ss_ts-doa-p_1_9

Locate and extract all the page elements that follow this XPath structure: "span" as HTML tag, "class" as attribute name, and "a-size-base-plus a-color-base a-text-normal" as the attribute value. You should also await 5 seconds between each element extraction in order to avoid request-related issues during the whole process. Finally, print all the human-readable text you got from those page elements as a list in the console.
```


## Script 3

```Text
Please web scrap the following page with Python, Selenium and ChromeDriver: https://x.com/biobio

Maximize the window (no headless mode). Locate and extract all the page elements that follow this XPath structure: "div" as HTML tag and "lang" as attribute name. You should also await 15 seconds between each element extraction in order to avoid request-related issues during the whole process. The page requires scrolling to get more elements to scrap. Print the text from each page element to the console.
```
