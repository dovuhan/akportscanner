import socket
from ipaddress import IPv4Network
import concurrent.futures


def scan_port(ip, port):
    """Bir IP'deki belirli bir portun açık olup olmadığını kontrol eder."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # 1 saniyelik zaman aşımı
        try:
            s.connect((ip, port))
            return port, True
        except:
            return port, False


def scan_ports_for_ip(ip, ports):
    """Bir IP'deki birden çok portu taramak için."""
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = {executor.submit(scan_port, ip, port): port for port in ports}

        for future in concurrent.futures.as_completed(results):
            port, status = future.result()
            if status:
                open_ports.append(port)

    return open_ports


def main():
    ip_range = input("IP adresini veya IP aralığını girin (örn. 192.168.1.1/24): ")
    start_port = int(input("Başlangıç portunu girin: "))
    end_port = int(input("Bitiş portunu girin: "))

    ports_to_scan = list(range(start_port, end_port + 1))

    for ip in IPv4Network(ip_range, strict=False):
        open_ports = scan_ports_for_ip(str(ip), ports_to_scan)
        if open_ports:
            print(f"{ip} üzerindeki açık portlar: {', '.join(map(str, open_ports))}")


if __name__ == "__main__":
    main()
