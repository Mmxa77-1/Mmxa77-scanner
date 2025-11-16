import socket
import concurrent.futures
from config import THREADS

def fast_scan_ports(target):
    # use ThreadPoolExecutor with THREADS
    ...

def grab_banner(target, port):
    """
    Attempts to grab the service banner from the target on the specified port.
    Returns the banner string or None.
    """
    try:
        sock = socket.socket()
        sock.settimeout(1)

        sock.connect((target, port))

        # Some services send banners immediately (FTP, SMTP, SSH)
        banner = sock.recv(1024).decode(errors="ignore").strip()

        sock.close()

        if banner:
            return banner
        else:
            return None

    except Exception:
        return None


def grab_banners_for_open_ports(target, open_ports):
    """
    Takes the list of (port, service) and tries to extract banners.
    Returns a dict: {port: banner}
    """
    banners = {}

    for port, svc in open_ports:
        banner = grab_banner(target, port)
        banners[port] = banner

    return banners
