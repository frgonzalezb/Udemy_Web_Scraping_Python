# XPath

Este módulo se desarrolla en [XPath Playground](https://scrapinghub.github.io/xpath-playground/).

Usa el siguiente ejemplo en HTML:

```html
<article class ="main-article">
    <h1> Titanic(1997) </h1>
    <p class ="plot" > 84 years later... </p>
    <p class ="plot2" > In the end ... </p>
    <div class ="full-script">
    "13 meters. You should see it. "
    "Okay, take her up and over the bow rail. "
    </div>
</article>
```

## Ejemplos de comandos

| XPath | Devuelve |
| ------------- | ------------- |
| `//h1` | `<h1> Titanic(1997) </h1>` |
| `//h1/text()` | `Titanic(1997)` |
| `//p[1]` | `<p class ="plot" > 84 years later... </p>` |
| `//p[@class="plot2"]/text()` | `In the end ...` |
| `//p[contains(@class, "plot2")]/text()` | `In the end ...` |

