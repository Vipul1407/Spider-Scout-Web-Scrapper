import threading
import queue

class URLFrontier:
    def __init__(self):
        self._queue = queue.Queue()
        self._visited = set()
        self._lock = threading.Lock()

    def add_url(self, url, depth=0):
        with self._lock:
            if url not in self._visited:
                self._visited.add(url)
                self._queue.put((url, depth))

    def add_urls(self, urls, depth=0):
        for u in urls:
            self.add_url(u, depth)

    def get_next(self, block=True, timeout=1):
        try:
            return self._queue.get(block=block, timeout=timeout)  # (url, depth)
        except queue.Empty:
            return None

    def task_done(self):
        try:
            self._queue.task_done()
        except Exception:
            pass

    def qsize(self):
        return self._queue.qsize()

    def visited_count(self):
        with self._lock:
            return len(self._visited)
