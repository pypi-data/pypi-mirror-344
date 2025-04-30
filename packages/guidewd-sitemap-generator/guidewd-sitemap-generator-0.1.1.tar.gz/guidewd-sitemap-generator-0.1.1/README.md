# Guidewd Sitemap Generator

**Guidewd Sitemap Generator** is a command-line tool designed to generate XML sitemaps for SEO optimization.  
It crawls websites, extracts URLs, and generates a sitemap that can be submitted to search engines like Google.

---

## Features

- Crawl a website to generate a sitemap
- Respect `robots.txt` rules (optional)
- Limit the number of pages to crawl
- Lightweight and easy to use from the command line
- Generates a standard XML sitemap format for SEO purposes

---

## Installation

You can install the package using pip:

```bash
pip install guidewd-sitemap-generator
```

---

## Usage
After installation, you can run the `guidewd-sitemap-generator` command directly from your terminal.

- Command-Line Interface:
```bash
guidewd-sitemap-generator <starting-url> --max-pages <max-pages> --respect-robots
```

- `<starting-url>`: The URL to start crawling from (e.g., `https://example.com`).
- `--max-pages <max-pages>`: Optional. Maximum number of pages to crawl (default: 200).
- `--respect-robots`: Optional. If specified, the tool will respect the site's `robots.txt` rules.

---

## Example

```bash
guidewd-sitemap-generator https://example.com --max-pages 100 --respect-robots
```

This will crawl the website starting from `https://example.com`, limit the crawl to 100 pages, and respect the `robots.txt` file.

---

## Input

- A valid website URL to start the crawl.

## Output

- An XML sitemap file (default: `sitemap.xml`) that contains a list of crawled URLs.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
