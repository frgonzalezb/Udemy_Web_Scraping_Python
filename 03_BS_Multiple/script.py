"""
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
