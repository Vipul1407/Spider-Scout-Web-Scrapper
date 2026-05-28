# SpiderScout 🕷️

A multithreaded, polite, and extensible web crawler built in Python for efficient web page crawling, parsing, indexing, and link discovery. SpiderScout follows `robots.txt` rules, supports concurrent crawling with worker threads, and generates a searchable crawl index.

The project implements core concepts used in real-world search engines and distributed crawlers such as URL frontier management, indexing, politeness policies, retry handling, and concurrent scheduling. 

---

# 📌 Features

* Multithreaded web crawling using worker threads
* URL Frontier for managing discovered URLs
* `robots.txt` compliance support
* Configurable crawl depth and page limits
* Politeness delay between requests to same host
* Automatic retry with exponential backoff
* HTML parsing using BeautifulSoup
* Link extraction and normalization
* Inverted indexing for fast search mapping
* Structured logging to console and log files
* JSON-based crawl index generation

---

# 🛠️ Tech Stack

* Python 3
* Requests
* BeautifulSoup4
* lxml
* Multithreading
* Queue-based scheduling

Dependencies used in the project: 

---

# 🧩 System Architecture

## Core Modules

### 1. URL Frontier

Handles URL queue management and duplicate prevention using thread-safe queues and visited tracking. 

### 2. Downloader

Responsible for downloading web pages with:

* Retry handling
* Exponential backoff
* Host-level politeness delay
* Timeout handling 

### 3. Parser

Extracts:

* Page title
* Clean text content
* Hyperlinks from HTML pages using BeautifulSoup. 

### 4. Robots.txt Handler

Checks crawling permissions before downloading pages by parsing website `robots.txt`. 

### 5. Scheduler

Coordinates worker threads and manages the complete crawling workflow. 

### 6. Indexer

Builds an inverted index and stores crawled documents in JSON format. 

### 7. Logger

Provides structured logging for crawl monitoring and debugging. 

---

# 🚀 How It Works

1. Seed URL is added to the URL Frontier
2. Scheduler creates multiple worker threads
3. Each worker:

   * Fetches URL from queue
   * Checks robots.txt permissions
   * Downloads page content
   * Parses links and text
   * Indexes extracted content
   * Adds discovered links back to frontier
4. Crawl continues until:

   * Max depth reached
   * Max pages reached
   * Queue becomes empty

---

# 📂 Project Structure

```bash
SpiderScout/
│── main.py
│── scheduler.py
│── downloader.py
│── parser.py
│── indexer.py
│── url_frontier.py
│── robots_txt_handler.py
│── logger_config.py
│── requirements.txt
│── crawl_index.json
│── spider_scout.log
```

---

# ⚙️ Installation

```bash
git clone <your-repo-link>
cd SpiderScout
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

Basic command:

```bash
python main.py --seed https://example.com
```

Advanced example:

```bash
python main.py \
  --seed https://www.python.org \
  --depth 3 \
  --workers 4 \
  --politeness 1.0 \
  --max-pages 100
```

CLI arguments supported by the crawler: 

| Argument       | Description               |
| -------------- | ------------------------- |
| `--seed`       | Starting URL              |
| `--depth`      | Maximum crawl depth       |
| `--workers`    | Number of crawler threads |
| `--politeness` | Delay between requests    |
| `--max-pages`  | Maximum pages to crawl    |

---

# 📊 Sample Output

The crawler generates:

## 1. `crawl_index.json`

Contains:

* Crawled documents
* Extracted text
* Links
* Inverted index statistics

Generated indexing structure: 

## 2. `spider_scout.log`

Contains detailed crawl logs:

* Download activity
* Indexed pages
* Failed downloads
* Crawl completion status 

---

# 🧠 Concepts Implemented

* Web Crawling
* Search Engine Indexing
* BFS-style URL Traversal
* Concurrent Programming
* Thread Synchronization
* Robots.txt Compliance
* Queue-based Scheduling
* Exponential Backoff
* Inverted Indexing

---

# 🔥 Future Improvements

* Distributed crawling support
* Page ranking algorithms
* Persistent database storage
* Domain filtering
* Duplicate content detection
* Async I/O implementation
* Search API over indexed pages
* Crawl visualization dashboard

---

# 🏷️ GitHub Repository Description

> Multithreaded Python web crawler with robots.txt compliance, concurrent scheduling, inverted indexing, and polite crawling support.

Alternative shorter version:

> A scalable multithreaded web crawler in Python with indexing, robots.txt handling, and concurrent crawling support.
