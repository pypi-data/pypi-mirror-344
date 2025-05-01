# WiniScraper

**WiniScraper** est un module de scraping rapide et ultra performant 

## Installation

```bash
pip install winiscraper
```

## Exemple d'utilisation

```python
from winiscraper import WiniScraper

scraper = WiniScraper("https://example.com")
scraper.fetch()

titre = scraper.select_one("title")
paragraphes = scraper.select("p")

print("Titre :", titre)
print("Paragraphes :", paragraphes)
```

## Fonctionnalités
- User-Agent intégré
- Rapide et léger
- Supporte les sélecteurs CSS
