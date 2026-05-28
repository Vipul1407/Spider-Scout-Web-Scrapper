import threading
import time
from logger_config import setup_logger

class Scheduler:
    def __init__(self, frontier, downloader, parser, indexer, robots_handler, logger=None, num_workers=4, max_pages=1000):
        self.frontier = frontier
        self.downloader = downloader
        self.parser = parser
        self.indexer = indexer
        self.robots = robots_handler
        self.num_workers = max(1, num_workers)
        self._stop_event = threading.Event()
        self.logger = logger or setup_logger()
        self.max_pages = max_pages
        self._active_workers = 0
        self._active_lock = threading.Lock()

    def _worker(self, max_depth):
        while not self._stop_event.is_set():
            item = self.frontier.get_next()
            if item is None:
                break
            url, depth = item
            try:
                if self.frontier.visited_count() > self.max_pages:
                    self.logger.info("Reached max_pages limit")
                    self._stop_event.set()
                    break

                if depth < 0:
                    continue

                if not self.robots.can_fetch(url):
                    self.logger.info(f"Blocked by robots.txt: {url}")
                    self.frontier.task_done()
                    continue

                self.logger.info(f"Downloading: {url} (depth {depth})")
                html = self.downloader.download(url)
                if not html:
                    self.logger.warning(f"Failed to download: {url}")
                    self.frontier.task_done()
                    continue

                links, title, text = self.parser.parse(html, url)
                self.indexer.index(url, title, text, links)
                self.logger.info(f"Indexed: {url} title={title!r} links_found={len(links)}")

                if depth + 1 <= max_depth:
                    for l in links:
                        self.frontier.add_url(l, depth + 1)

            except Exception as e:
                self.logger.exception(f"Error processing {url}: {e}")
            finally:
                self.frontier.task_done()
        with self._active_lock:
            self._active_workers -= 1

    def crawl(self, seed_url, max_depth=2):
        self.frontier.add_url(seed_url, depth=0)
        self.logger.info(f"Starting crawl seed={seed_url} max_depth={max_depth} workers={self.num_workers}")
        threads = []
        with self._active_lock:
            self._active_workers = self.num_workers
        for _ in range(self.num_workers):
            t = threading.Thread(target=self._worker, args=(max_depth,), daemon=True)
            threads.append(t)
            t.start()

        try:
            while any(t.is_alive() for t in threads):
                time.sleep(0.5)
                if self._stop_event.is_set():
                    break
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt: stopping crawl")
            self._stop_event.set()

        for t in threads:
            t.join(timeout=1)

        self.indexer.save()
        self.logger.info("Crawl finished. Results saved.")
