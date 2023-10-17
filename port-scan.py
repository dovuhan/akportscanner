import socket
from ipaddress import IPv4Network
import concurrent.futures

def get_service(port):
    """Port numarasına göre yaygın servis adını döndürür."""
    service_name = socket.getservbyport(port, 'tcp')
    return service_name or 'Unknown'


def scan_port(ip, port):
    """Bir IP'deki belirli bir portun açık olup olmadığını kontrol eder."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((ip, port))
            service = get_service(port)
            return port, True, service
        except:
            return port, False, ''


def scan_ports_for_ip(ip, ports):
    """Bir IP'deki birden çok portu taramak için."""
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = {executor.submit(scan_port, ip, port): port for port in ports}

        for future in concurrent.futures.as_completed(results):
            port, status, service = future.result()
            if status:
                open_ports.append((port, service))

    return open_ports


def main():
    ip_range = input("IP adresini veya IP aralığını girin (örn. 192.168.1.1/24): ")
    start_port = int(input("Başlangıç portunu girin: "))
    end_port = int(input("Bitiş portunu girin: "))

    ports_to_scan = list(range(start_port, end_port + 1))
    all_ips = list(IPv4Network(ip_range, strict=False))

    for index, ip in enumerate(all_ips, 1):
        print(f"{index}/{len(all_ips)} - {ip} taranıyor...")
        open_ports = scan_ports_for_ip(str(ip), ports_to_scan)
        if open_ports:
            port_strings = [f"{port} ({service})" for port, service in open_ports]
            print(f"{ip} üzerindeki açık portlar: {', '.join(port_strings)}")


if __name__ == "__main__":
    main()
