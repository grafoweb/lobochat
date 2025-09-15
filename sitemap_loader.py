import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from typing import List, Dict

HEADERS = {"User-Agent": "LoboAndCompanyBot/1.0 (+https://loboandco.com)"}
EXCLUDE_PATTERNS = ["/wp-login", "/wp-admin", "/cart", "/checkout", "/my-account"]
MAX_PAGES = 200
TIMEOUT = 15

def fetch_page_text(url: str) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "noscript"]):
            tag.decompose()
        main = soup.find("main") or soup.body or soup
        text = main.get_text(separator=" ", strip=True)
        return text
    except Exception as e:
        return f"[ERROR] No se pudo leer {url}: {e}"

def parse_sitemap(sitemap_url: str) -> List[str]:
    resp = requests.get(sitemap_url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [elem.text for elem in root.iter(f"{ns}loc")] or [elem.text for elem in root.iter() if "loc" in elem.tag]
    cleaned = [u for u in urls if not any(p in u for p in EXCLUDE_PATTERNS)]
    return cleaned

def load_from_sitemap(sitemap_url: str) -> List[Dict[str, str]]:
    urls = parse_sitemap(sitemap_url)
    pages: List[Dict[str, str]] = []
    for url in urls[:MAX_PAGES]:
        text = fetch_page_text(url)
        pages.append({"url": url, "text": text})
    return pages
