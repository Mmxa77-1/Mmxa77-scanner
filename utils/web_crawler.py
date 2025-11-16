import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import HTTP_TIMEOUT, MAX_PAGES


async def fetch(session, url):
    """Fetch a page asynchronously."""
    try:
        async with session.get(url, timeout=HTTP_TIMEOUT) as resp:
            return url, await resp.text()
    except:
        return url, None


async def crawl_async(start_url):
    """Async fast crawler."""
    visited = set()
    to_visit = [start_url]
    pages = {}

    async with aiohttp.ClientSession() as session:
        while to_visit and len(visited) < MAX_PAGES:
            tasks = [fetch(session, url) for url in to_visit]
            to_visit = []
            results = await asyncio.gather(*tasks)

            for url, html in results:
                if not html:
                    continue

                visited.add(url)
                pages[url] = html

                soup = BeautifulSoup(html, "html.parser")

                for link in soup.find_all("a", href=True):
                    abs_url = urljoin(url, link["href"])
                    if abs_url not in visited and abs_url.startswith(start_url):
                        to_visit.append(abs_url)

    return pages


def crawl_website(url):
    """Sync wrapper for async crawler."""
    return asyncio.run(crawl_async(url))
