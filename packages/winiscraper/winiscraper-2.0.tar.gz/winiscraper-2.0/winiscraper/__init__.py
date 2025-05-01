import httpx
from selectolax.parser import HTMLParser

class WiniScraper:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "User-Agent": "WiniScraper"
        }
        self.html = None
        self.parser = None

    def fetch(self):
        response = httpx.get(self.url, headers=self.headers)
        response.raise_for_status()
        self.html = response.text
        self.parser = HTMLParser(self.html)

    def select(self, selector: str):
        if not self.parser:
            raise Exception("Appelle .fetch() avant d'utiliser .select()")
        return [node.text(strip=True) for node in self.parser.css(selector)]

    def select_one(self, selector: str):
        if not self.parser:
            raise Exception("Appelle .fetch() avant d'utiliser .select_one()")
        node = self.parser.css_first(selector)
        return node.text(strip=True) if node else None
