from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse
import re

class Parser:
    def __init__(self):
        pass

    def parse(self, html, base_url):
        """
        Returns:
            links: set of normalized absolute URLs
            title: page title or empty string
            text: cleaned text content
        """
        soup = BeautifulSoup(html, "lxml")
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        raw_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("mailto:") or href.startswith("javascript:"):
                continue
            abs_url = urljoin(base_url, href)
            abs_url, _ = urldefrag(abs_url)
            parsed = urlparse(abs_url)
            if parsed.scheme not in ("http", "https"):
                continue
            raw_links.add(abs_url)

        for s in soup(["script", "style", "noscript"]):
            s.extract()
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        return raw_links, title, text
