#!/usr/bin/env python3

import argparse
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import urllib.robotparser

VALID_EXTENSIONS = ('.html', '.php', '.htm', '/')
FOLLOW_EXTERNAL = False
OUTPUT_FILE = "sitemap.xml"

visited = set()
queue = []
sitemap_urls = []
broken_links = []

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

def fetch_links(url):
    try:
        with urlopen(url, timeout=10) as response:
            if 'text/html' not in response.getheader('Content-Type', ''):
                return []
            html = response.read().decode(errors='ignore')
            parser = LinkParser()
            parser.feed(html)
            return parser.links
    except Exception as e:
        broken_links.append((url, str(e)))
        return []

def should_visit(url, domain, robot_parser, respect_robots):
    parsed = urlparse(url)
    if not FOLLOW_EXTERNAL and parsed.netloc and parsed.netloc != domain:
        return False
    if not url.endswith(VALID_EXTENSIONS):
        return False
    if respect_robots:
        return robot_parser.can_fetch("*", url)
    return True

def load_robots_txt(start_url):
    parsed = urlparse(start_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception as e:
        print(f"⚠️ Could not read robots.txt: {e}")
    return rp

def generate_sitemap(start_url, max_pages, respect_robots):
    print("🎉 Thank you for using the GuideWD Sitemap Generator Tool!")
    print("🔧 Designed by the Raghava Lab as an open-source tool to generate sitemaps.")
    print(f"🌐 Starting crawl from: {start_url}\n")

    domain = urlparse(start_url).netloc
    queue.append(start_url)
    robot_parser = load_robots_txt(start_url) if respect_robots else urllib.robotparser.RobotFileParser()

    while queue and len(sitemap_urls) < max_pages:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        print(f"🔍 Crawling: {current}")
        links = fetch_links(current)
        sitemap_urls.append(current)
        for link in links:
            abs_link = urljoin(current, link).split('#')[0]
            if should_visit(abs_link, domain, robot_parser, respect_robots) and abs_link not in visited:
                queue.append(abs_link)

    # Write sitemap
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url in sitemap_urls:
        url_el = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_el, "loc")
        loc.text = url
    tree = ET.ElementTree(urlset)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

    print(f"\n✅ Sitemap generated with {len(sitemap_urls)} pages.")
    print(f"📄 Saved to {OUTPUT_FILE}")

    if broken_links:
        print("\n⚠️ Broken links found:")
        for url, reason in broken_links:
            print(f" - {url}: {reason}")

def main():
    parser = argparse.ArgumentParser(description="GuideWD Sitemap CLI Generator")
    parser.add_argument("url", help="Starting URL for sitemap generation")
    parser.add_argument("--max-pages", type=int, default=200, help="Maximum number of pages to crawl (default: 200)")
    parser.add_argument("--respect-robots", action="store_true", help="Respect robots.txt rules (default: False)")
    args = parser.parse_args()

    generate_sitemap(args.url, args.max_pages, args.respect_robots)

if __name__ == "__main__":
    main()
