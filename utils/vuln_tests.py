import aiohttp
import asyncio
from config import ACTIVE_TESTS, HTTP_TIMEOUT

XSS_PAYLOADS = ["<script>alert(1)</script>", "\"'><script>alert(1)</script>"]
SQLI_PAYLOADS = ["'", "\"", "1 OR 1=1", "' OR '1'='1"]


async def test_payload(session, url):
    """Try loading URL and capture page."""
    try:
        async with session.get(url, timeout=HTTP_TIMEOUT) as resp:
            return url, await resp.text()
    except:
        return url, None


async def test_params_async(base_url, param, value):
    """Test XSS + SQLi on a single parameter."""
    issues = []
    urls = []

    # build attack URLs
    if ACTIVE_TESTS:
        for payload in XSS_PAYLOADS + SQLI_PAYLOADS:
            urls.append(f"{base_url}?{param}={payload}")

    async with aiohttp.ClientSession() as session:
        tasks = [test_payload(session, u) for u in urls]
        results = await asyncio.gather(*tasks)

        for test_url, html in results:
            if not html:
                continue

            # detect reflected payload (XSS)
            for p in XSS_PAYLOADS:
                if p in html:
                    issues.append((test_url, "Reflected XSS"))

            # detect SQL errors
            db_errors = ["sql", "mysql", "syntax error", "pdo"]
            if any(err in html.lower() for err in db_errors):
                issues.append((test_url, "Possible SQL Injection"))

    return issues


def test_parameters(url, params):
    """Sync wrapper."""
    findings = []

    for param in params:
        results = asyncio.run(test_params_async(url, param, "test"))
        findings.extend(results)

    return findings
