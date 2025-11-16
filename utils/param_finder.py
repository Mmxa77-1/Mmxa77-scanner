# utils/param_finder.py
from urllib.parse import urlparse, parse_qs, unquote
from bs4 import BeautifulSoup
import re
import concurrent.futures

# Regex to find parameters in JS or HTML links
PARAM_REGEX = re.compile(r"[?&]([a-zA-Z0-9_\-]+)=")

def extract_query_params(url):
    """Extract GET parameters from URL query string."""
    q = urlparse(url).query
    if not q:
        # Also check JS/embedded params
        matches = PARAM_REGEX.findall(url)
        return list(set(matches))
    parsed = parse_qs(q)
    return list(parsed.keys())

def extract_form_inputs(html):
    """Extract all form input names from HTML."""
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    inputs = []
    for form in soup.find_all("form"):
        for inp in form.find_all(["input", "textarea", "select"]):
            name = inp.get("name")
            if name:
                inputs.append(name)
    return inputs

def find_parameters_for_page(url_html_tuple):
    """Process a single page: extract GET + POST/form parameters."""
    url, html = url_html_tuple
    params = set()

    # 1. Extract GET parameters
    params.update(extract_query_params(url))

    # 2. Extract form inputs
    form_inputs = extract_form_inputs(html)
    params.update(form_inputs)

    # 3. Extract JS embedded params
    if html:
        js_matches = PARAM_REGEX.findall(html)
        params.update(js_matches)

    return url, list(params)

def find_parameters(pages, threads=20):
    """
    Extract parameters from all pages using multithreading.
    Returns: {url: [param1, param2, ...]}
    """
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = executor.map(find_parameters_for_page, pages.items())

        for url, params in futures:
            results[url] = params

    return results
