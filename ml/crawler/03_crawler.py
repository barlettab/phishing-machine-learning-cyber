import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# =========================
# CONFIG
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DOMAINS_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "datasets",
    "processed",
    "domains.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "datasets",
    "processed",
    "legitimate_urls.csv"
)

LOG_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "datasets",
    "processed",
    "crawler_log.txt"
)

MAX_URLS_PER_DOMAIN = 15
MAX_DEPTH = 2
TIMEOUT = 10
SLEEP_BETWEEN_REQUESTS = 0.5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (DatasetCrawler/1.0)"
}

# =========================
# UTILS
# =========================

def log(msg):
    print(msg)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def normalize_url(base, link):
    return urljoin(base, link)


def is_valid_url(url, domain):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ["http", "https"]:
            return False

        if domain not in parsed.netloc:
            return False

        if any(x in url.lower() for x in [
            "javascript:",
            "mailto:",
            "tel:"
        ]):
            return False

        return True

    except:
        return False


def extract_links(html, base_url, domain):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        url = normalize_url(base_url, tag["href"])

        if is_valid_url(url, domain):
            links.add(url)

    return list(links)


# =========================
# CRAWLER CORE
# =========================

def crawl_domain(domain):
    visited = set()
    to_visit = [(f"https://{domain}", 0)]
    collected = []

    while to_visit and len(collected) < MAX_URLS_PER_DOMAIN:

        url, depth = to_visit.pop(0)

        if url in visited or depth > MAX_DEPTH:
            continue

        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

            if response.status_code != 200:
                continue

            html = response.text
            visited.add(url)
            collected.append(url)

            time.sleep(SLEEP_BETWEEN_REQUESTS)

            if depth < MAX_DEPTH:
                links = extract_links(html, url, domain)

                for link in links:
                    if link not in visited:
                        to_visit.append((link, depth + 1))

        except Exception as e:
            log(f"[ERROR] {domain} -> {url} | {str(e)}")
            continue

    return collected


# =========================
# MAIN
# =========================

def main():

    # reset log
    open(LOG_PATH, "w").close()

    df = pd.read_csv(DOMAINS_PATH)

    domains = df["Domain"].dropna().tolist()

    all_urls = []

    log(f"Starting crawler with {len(domains)} domains")

    for i, domain in enumerate(domains):

        log(f"[{i+1}/{len(domains)}] Crawling: {domain}")

        urls = crawl_domain(domain)

        log(f"   -> collected: {len(urls)} URLs")

        for url in urls:
            all_urls.append({
                "url": url,
                "label": 0
            })

        # salva incremental (IMPORTANTÍSSIMO)
        if i % 100 == 0 and i > 0:
            pd.DataFrame(all_urls).to_csv(OUTPUT_PATH, index=False)

    # final save
    pd.DataFrame(all_urls).to_csv(OUTPUT_PATH, index=False)

    log("DONE")
    log(f"Total URLs collected: {len(all_urls)}")


if __name__ == "__main__":
    main()