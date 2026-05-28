import argparse
from logger_config import setup_logger
from url_frontier import URLFrontier
from downloader import Downloader
from parser import Parser
from indexer import Indexer
from robots_txt_handler import RobotsTxtHandler
from scheduler import Scheduler


def main():
    parser = argparse.ArgumentParser(description="Spider Scout crawler")
    parser.add_argument("--seed", required=True,
                        help="Seed URL to start crawling from")
    parser.add_argument("--depth", type=int, default=2, help="Max crawl depth")
    parser.add_argument("--workers", type=int, default=4,
                        help="Number of worker threads")
    parser.add_argument("--politeness", type=float, default=1.0,
                        help="Seconds between requests to same host")
    parser.add_argument("--max-pages", type=int, default=1000,
                        help="Maximum pages to crawl (safety limit)")
    args = parser.parse_args()

    logger = setup_logger()
    frontier = URLFrontier()
    downloader = Downloader(politeness=args.politeness)
    parser_module = Parser()
    indexer = Indexer()
    robots = RobotsTxtHandler()

    sched = Scheduler(frontier, downloader, parser_module, indexer, robots,
                      logger=logger, num_workers=args.workers, max_pages=args.max_pages)
    sched.crawl(args.seed, max_depth=args.depth)


if __name__ == "__main__":
    main()
