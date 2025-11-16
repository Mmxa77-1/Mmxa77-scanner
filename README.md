Mmxa77 Fast Vulnerability Scanner 🚀

A fast, modular, and professional web vulnerability scanner written in Python.
It can perform port scanning, banner grabbing, header checks, TLS analysis, crawling, parameter detection, and active vulnerability testing (XSS/SQLi).

Features :

-Fast Port Scanning with customizable speed
-Banner Grabbing for open ports
-HTTP Header Analysis to detect missing security headers
-TLS/SSL Check for HTTPS sites
-Website Crawling (async, fast)
-GET & POST Parameter Extraction including forms and JS-based parameters
-Active Vulnerability Testing for XSS & SQL injection
-JSON Report Generation for easy analysis
-Colorful CLI Output & Progress Bars for better readability

Installation :

1️⃣ Clone the repository
git clone https://github.com/your-username/Mmxa77-scanner.git
cd Mmxa77-scanner

2️⃣ Create a virtual environment
python3 -m venv scanner_venv
source scanner_venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

Usage :
python megascan.py -u <target_url>

Example:

python megascan.py -u testphp.vulnweb.com

Progress bars will show crawling, banner grabbing, and parameter testing.

Vulnerabilities, if any, are displayed in red.

Results are saved automatically in:

reports/results.json

Directory Structure
Mmxa77-scanner/
│
├─ megascan.py       
├─ config.py                     
├─ README.md
├─ requirements.txt               
│
├─ utils/                         
│  ├─ banner_grabber.py
│  ├─ header_checker.py
│  ├─ param_finder.py
│  ├─ port_scanner.py
│  ├─ reports.py
│  ├─ tls_checker.py
│  ├─ vuln_tests.py
│  └─ web_crawler.py
│
└─ reports/
   └─ results.json    
   
License :

-This project is licensed under the MIT License – see the LICENSE
 file for details.

Notes :

-Only scan websites you own or have permission to test.

-Perfect for learning, testing.

-Works best in Kali-Linux.            
