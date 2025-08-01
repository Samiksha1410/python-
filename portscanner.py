# -*- coding: utf-8 -*-
"""portscanner.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b3gk73OlHc2V01Bs5RRx3PqMsgJrtCTE
"""

import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Store results
open_ports = []

# Banner grabbing
def get_banner(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=1) as sock:
            sock.settimeout(1)
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner
    except:
        return "No banner"

# Port scanning logic
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                banner = get_banner(ip, port)
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"
                open_ports.append((port, service, banner))
    except Exception as e:
        pass

# Display results
def print_results():
    print(f"\n{'Port':<10}{'Service':<20}{'Banner'}")
    print("-" * 60)
    for port, service, banner in sorted(open_ports):
        print(f"{port:<10}{service:<20}{banner}")

# Main logic
def main():
    ip = input("Enter target IP address: ").strip()
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    print(f"\nStarting scan on {ip} from port {start_port} to {end_port}")
    print("Scanning...\n")
    start_time = datetime.now()

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port)

    print_results()

    duration = datetime.now() - start_time
    print(f"\nScan completed in: {duration}")

if __name__ == "__main__":
    main()

