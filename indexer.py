import json
import threading
from collections import defaultdict

class Indexer:
    def __init__(self):
        self._lock = threading.Lock()
        self.documents = {}  # url -> {title, text, links}
        self.inverted = defaultdict(set)

    def index(self, url, title, text, links):
        with self._lock:
            self.documents[url] = {"title": title, "text": text, "links": list(links)}
            tokens = set(word.lower() for word in text.split() if len(word) > 2)
            for t in tokens:
                self.inverted[t].add(url)

    def save(self, out_file="crawl_index.json"):
        with self._lock:
            dump = {"documents": self.documents, "inverted_index_counts": {k: len(v) for k,v in self.inverted.items()}}
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(dump, f, indent=2, ensure_ascii=False)

    def get_doc(self, url):
        with self._lock:
            return self.documents.get(url)
