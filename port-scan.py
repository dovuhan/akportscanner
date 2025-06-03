import argparse
import json
import socket
from ipaddress import ip_network
import concurrent.futures
from typing import List, Tuple


def get_service(port: int) -> str:
    """Return common service name for a given TCP port."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Unknown"


def scan_tcp_port(ip: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str]:
    """Check if a TCP port is open on an IP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((ip, port))
            return port, True, get_service(port)
        except Exception:
            return port, False, ""


def scan_ports_for_ip(ip: str, ports: List[int], workers: int) -> List[Tuple[int, str]]:
    """Scan multiple ports for a single IP."""
    open_ports: List[Tuple[int, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_tcp_port, ip, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            port, status, service = future.result()
            if status:
                open_ports.append((port, service))
    return open_ports


def parse_ports(ports_str: str) -> List[int]:
    """Parse a port string like '80,443,8000-8100' into a list of ints."""
    ports: List[int] = []
    for part in ports_str.split(','):
        if '-' in part:
            start, end = part.split('-', 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple multithreaded port scanner")
    parser.add_argument('-t', '--target', required=True, help='IP address or range e.g. 192.168.1.1/24')
    parser.add_argument('-p', '--ports', required=True, help='Port(s) to scan e.g. 22,80,1-100')
    parser.add_argument('-w', '--workers', type=int, default=100, help='Number of threads')
    parser.add_argument('-o', '--output', help='Output results to JSON file')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ports = parse_ports(args.ports)
    network = ip_network(args.target, strict=False)

    results = {}
    for index, ip in enumerate(network, 1):
        print(f"{index}/{network.num_addresses} - scanning {ip} ...")
        open_ports = scan_ports_for_ip(str(ip), ports, args.workers)
        if open_ports:
            results[str(ip)] = open_ports
            ports_str = ', '.join(f"{p} ({svc})" for p, svc in open_ports)
            print(f"  Open ports: {ports_str}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Results written to {args.output}")


if __name__ == '__main__':
    main()
