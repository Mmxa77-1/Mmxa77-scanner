import socket
import concurrent.futures
from config import THREADS, PORT_TIMEOUT

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 3389: "RDP"
}

def scan_single_port(target, port):
    """Scan a single port quickly."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(PORT_TIMEOUT)
        sock.connect((target, port))
        sock.close()
        return port, COMMON_PORTS.get(port, "Unknown")
    except:
        return None


def fast_scan_ports(target):
    """Fast multithreaded port scanning."""
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(lambda p: scan_single_port(target, p), COMMON_PORTS.keys())

        for result in results:
            if result:
                open_ports.append(result)

    return open_ports
