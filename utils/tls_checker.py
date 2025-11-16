import ssl
import socket
from datetime import datetime

def check_tls(target, port=443):
    """
    Connects to the server using SSL/TLS and retrieves certificate details.
    Returns dict with TLS info and issues.
    """
    context = ssl.create_default_context()

    try:
        with socket.create_connection((target, port), timeout=4) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                tls_version = ssock.version()

        results = {
            "target": target,
            "port": port,
            "tls_version": tls_version,
            "certificate": cert,
            "issues": []
        }

        # --- Check for weak TLS versions ---
        if tls_version in ["TLSv1", "TLSv1.1"]:
            results["issues"].append(f"Weak TLS version detected: {tls_version} (deprecated)")

        # --- Certificate expiration check ---
        expires = cert.get("notAfter", None)
        if expires:
            exp_date = datetime.strptime(expires, "%b %d %H:%M:%S %Y %Z")
            days_left = (exp_date - datetime.utcnow()).days
            results["expires_in_days"] = days_left
            if days_left < 0:
                results["issues"].append("Certificate is expired!")
            elif days_left < 30:
                results["issues"].append(f"Certificate expires soon: {days_left} days left")

        # --- Key length check ---
        # Not all certificates expose key length cleanly
        # We'll take a safe guess using subject and issuer
        issuer = cert.get("issuer")
        subject = cert.get("subject")
        results["issuer"] = issuer
        results["subject"] = subject

        return results

    except Exception as e:
        return {"error": str(e)}
