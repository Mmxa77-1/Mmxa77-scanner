import json
import os
from datetime import datetime

def save_results(target, open_ports, banners, headers, tls, pages, findings, path="reports/results.json"):
    """
    Save scanner results in a structured JSON 'tableau' format.
    
    - target: target domain/IP
    - open_ports: list of (port, service)
    - banners: dict {port: banner}
    - headers: dict of HTTP headers and missing headers
    - tls: dict TLS info
    - pages: dict {url: html} or page info
    - findings: list of vulnerabilities
    """

    # Build table-like structure
    result_table = {
        "target": target,
        "scan_time": datetime.utcnow().isoformat() + "Z",
        "open_ports": [{"port": p[0], "service": p[1], "banner": banners.get(p[0])} for p in open_ports],
        "http_headers": headers,
        "tls": tls,
        "pages": [],
        "vulnerabilities": []
    }

    # Pages & parameters
    for url, html in pages.items():
        page_entry = {"url": url, "params": [], "issues": []}
        # If you have param extraction already
        if hasattr(pages, "params") and url in pages.params:
            page_entry["params"] = pages.params[url]
        result_table["pages"].append(page_entry)

    # Vulnerabilities
    for f in findings:
        result_table["vulnerabilities"].append({
            "url": f[0] if isinstance(f, tuple) else "",
            "issue": f[1] if isinstance(f, tuple) else str(f)
        })

    # Save JSON
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result_table, f, indent=4, ensure_ascii=False)

    print(f"[+] Results saved to {path}")
