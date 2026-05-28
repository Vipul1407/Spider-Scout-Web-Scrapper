import urllib.robotparser
from urllib.parse import urlparse
import time
import requests


class RobotsTxtHandler:
    def __init__(self, user_agent="SpiderScoutBot", cache_ttl=3600):
        self.user_agent = user_agent
        self._parsers = {}
        self._timestamps = {}
        self._cache_ttl = cache_ttl

    def _get_base(self, url):
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}"

    def _fetch_parser(self, base_url):
        now = time.time()
        if base_url in self._parsers and (now - self._timestamps.get(base_url, 0)) < self._cache_ttl:
            return self._parsers[base_url]

        robots_url = base_url.rstrip("/") + "/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = requests.get(robots_url, timeout=5)
            if r.status_code == 200:
                rp.parse(r.text.splitlines())
            else:
                rp = None
        except Exception:
            rp = None

        self._parsers[base_url] = rp
        self._timestamps[base_url] = now
        return rp

    def can_fetch(self, url):
        base = self._get_base(url)
        rp = self._fetch_parser(base)
        if rp is None:
            return True
        try:
            return rp.can_fetch(self.user_agent, url)
        except Exception:
            return True
