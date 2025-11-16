import requests

REQUIRED_HEADERS = {
    "Strict-Transport-Security": "Prevents SSL stripping attacks",
    "X-Content-Type-Options": "Prevents MIME-type sniffing",
    "Content-Security-Policy": "Mitigates XSS attacks",
    "X-Frame-Options": "Prevents clickjacking",
    "Referrer-Policy": "Controls referer data leakage",
}

def check_security_headers(url):
    """
    Sends a GET request to the URL and analyzes security headers.
    Returns a dict with found/missing headers.
    """

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=3)
        headers = response.headers

        results = {
            "url": url,
            "status_code": response.status_code,
            "present": {},
            "missing": {},
            "server_header": headers.get("Server", "Not provided")
        }

        for header, description in REQUIRED_HEADERS.items():
            if header in headers:
                results["present"][header] = headers[header]
            else:
                results["missing"][header] = description

        return results

    except Exception as e:
        return {"error": str(e)}
