from utils.port_scanner import fast_scan_ports
from utils.banner_grabber import grab_banners_for_open_ports
from utils.header_checker import check_security_headers
from utils.tls_checker import check_tls
from utils.web_crawler import crawl_website
from utils.param_finder import find_parameters
from utils.vuln_tests import test_parameters
from utils.reports import save_results

from colorama import init, Fore, Style
from tqdm import tqdm
import argparse

# Initialize colorama
init(autoreset=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, help="Target website URL")
    args = parser.parse_args()

    target = args.url
    print(Fore.CYAN + "=== FAST Vulnerability Scanner ===")
    print(Fore.CYAN + f"[+] Target: {target}")

    # -----------------------------
    # 1. Fast Port Scan
    # -----------------------------
    print(Fore.CYAN + "\n[+] Scanning ports (FAST MODE)...")
    open_ports = fast_scan_ports(target)
    print(Fore.GREEN + f"[+] Ports found: {open_ports}")

    # -----------------------------
    # 2. Banner grabbing
    # -----------------------------
    print(Fore.CYAN + "\n[+] Grabbing banners...")
    banners = {}
    for port in tqdm(open_ports, desc="Banner grabbing", unit="port"):
        b = grab_banners_for_open_ports(target, [port])
        banners.update(b)
    print(Fore.GREEN + f"[+] Banners: {banners}")

    # -----------------------------
    # 3. HTTP header check
    # -----------------------------
    print(Fore.CYAN + "\n[+] Checking HTTP security headers...")
    headers = check_security_headers(target)
    print(Fore.YELLOW + f"[+] Headers: {headers}")

    # -----------------------------
    # 4. TLS check
    # -----------------------------
    print(Fore.CYAN + "\n[+] Checking TLS/SSL...")
    tls = check_tls(target)
    if "error" in tls:
        print(Fore.RED + f"[!] TLS error: {tls['error']}")
    else:
        print(Fore.GREEN + f"[+] TLS info: {tls}")

    # -----------------------------
    # 5. Fast crawling
    # -----------------------------
    print(Fore.CYAN + "\n[+] Crawling website (FAST MODE)...")
    pages = crawl_website(target)
    for _ in tqdm(pages, desc="Pages crawled", unit="page"):
        pass
    print(Fore.GREEN + f"[+] Crawled {len(pages)} pages")

    # -----------------------------
    # 6. Parameter extraction
    # -----------------------------
    print(Fore.CYAN + "\n[+] Detecting query/form parameters...")
    params = find_parameters(pages)
    for _ in tqdm(params, desc="Extracting parameters", unit="page"):
        pass
    print(Fore.GREEN + f"[+] Parameters found: {params}")

    # -----------------------------
    # 7. Active vuln tests (XSS/SQLi)
    # -----------------------------
    print(Fore.CYAN + "\n[+] Running parameter tests...")
    findings = []
    for url in tqdm(pages, desc="Testing parameters", unit="page"):
        page_params = params.get(url, [])
        results = test_parameters(url, page_params)
        findings.extend(results)

    print(Fore.RED + "\nVulnerabilities Found:")
    if not findings:
        print(Fore.GREEN + "[+] No vulnerabilities detected")
    else:
        for f in findings:
            print(Fore.RED + f"[!] {f}")

    # -----------------------------
    # 8. Save results
    # -----------------------------
    print(Fore.CYAN + "\n[+] Saving results...")
    save_results(target, open_ports, banners, headers, tls, pages, findings)
    print(Fore.GREEN + "[+] Results saved successfully in reports/results.json!")


if __name__ == "__main__":
    main()
