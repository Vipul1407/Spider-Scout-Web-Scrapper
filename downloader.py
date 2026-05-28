import requests
import time
from urllib.parse import urlparse
import threading

class Downloader:
    def __init__(self, user_agent="SpiderScoutBot", timeout=8, max_retries=2, politeness=1.0):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self.timeout = timeout
        self.max_retries = max_retries
        self.politeness = politeness
        self._host_locks = {}
        self._host_last_access = {}
        self._lock = threading.Lock()

    def _host_for(self, url):
        p = urlparse(url)
        return p.netloc

    def _wait_politeness(self, host):
        with self._lock:
            last = self._host_last_access.get(host, 0)
            wait = max(0.0, self.politeness - (time.time() - last))
            if wait > 0:
                time.sleep(wait)
            self._host_last_access[host] = time.time()

    def download(self, url):
        host = self._host_for(url)
        with self._lock:
            if host not in self._host_locks:
                self._host_locks[host] = threading.Lock()

        with self._host_locks[host]:
            self._wait_politeness(host)
            attempt = 0
            backoff = 1.0
            while attempt <= self.max_retries:
                try:
                    r = self.session.get(url, timeout=self.timeout)
                    if r.status_code == 200:
                        return r.text
                    else:
                        attempt += 1
                        time.sleep(backoff)
                        backoff *= 2
                except requests.RequestException:
                    attempt += 1
                    time.sleep(backoff)
                    backoff *= 2
            return None
