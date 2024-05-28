import requests
import socket
import ssl
import whois
import dns.resolver
import subprocess
import json

class NetworkEntityInformation:
    def __init__(self, ip, api_key=None):
        self.ip = ip
        self.api_key = api_key

    def fetch_ip_geolocation(self):
        try:
            ip_info = None
            if self.api_key:
                response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}&ip={self.ip}')
                if response.status_code == 200:
                    ip_info = response.json()
                else:
                    print(f"Failed to get IP info for {self.ip}: Status code {response.status_code}")
            return ip_info
        except Exception as e:
            print(f"Failed to get IP info for {self.ip}: {str(e)}")

    def reverse_dns_lookup(self):
        try:
            return socket.gethostbyaddr(self.ip)[0]
        except Exception as e:
            print(f"Failed to perform reverse DNS lookup for {self.ip}: {str(e)}")

    def ping_test(self):
        try:
            subprocess.run(['ping', '-c', '4', self.ip])
        except Exception as e:
            print(f"Ping test failed for {self.ip}: {str(e)}")

    def traceroute(self, destination_ip):
        try:
            subprocess.run(['traceroute', self.ip, destination_ip])
        except Exception as e:
            print(f"Traceroute failed for {self.ip}: {str(e)}")

    def port_scan(self, start_port=1, end_port=1024):
        try:
            open_ports = []
            for port in range(start_port, end_port+1):
                sock = socket.socket(socket.AF_INET6 if ':' in self.ip else socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((self.ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            return open_ports
        except Exception as e:
            print(f"Port scan failed for {self.ip}: {str(e)}")

    def banner_grab(self, port):
        try:
            with socket.socket(socket.AF_INET6 if ':' in self.ip else socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((self.ip, port))
                s.send(b"GET / HTTP/1.1\r\n\r\n")
                banner = s.recv(1024).decode('utf-8')
            return banner.strip()
        except Exception as e:
            print(f"Failed to grab banner for port {port}: {str(e)}")

    def ssl_certificate_info(self, port=443):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.ip, port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.ip) as ssock:
                    cert = ssock.getpeercert()
                    return cert
        except Exception as e:
            print(f"Failed to fetch SSL certificate info for {self.ip}: {str(e)}")

    def http_headers(self):
        try:
            response = requests.get(f"http://{self.ip}")
            return dict(response.headers)
        except Exception as e:
            print(f"Failed to fetch HTTP headers for {self.ip}: {str(e)}")

    def whois_info(self):
        try:
            return whois.whois(self.ip)
        except Exception as e:
            print(f"Failed to fetch whois info for {self.ip}: {str(e)}")

    def dns_records(self):
        try:
            return [str(record) for record in dns.resolver.resolve(self.ip, 'A')]
        except Exception as e:
            print(f"Failed to fetch DNS records for {self.ip}: {str(e)}")

    def passive_scan(self):
        try:
            open_ports = self.port_scan()
            banner_info = {}
            ssl_info = {}
            http_headers_info = {}
            for port in open_ports:
                banner_info[port] = self.banner_grab(port)
                if port == 443:  # If it's an HTTPS port
                    ssl_info[port] = self.ssl_certificate_info(port)
                if port == 80:   # If it's an HTTP port
                    http_headers_info[port] = self.http_headers()
            return {
                'open_ports': open_ports,
                'banner_info': banner_info,
                'ssl_info': ssl_info,
                'http_headers_info': http_headers_info
            }
        except Exception as e:
            print(f"Passive scan failed for {self.ip}: {str(e)}")

    def active_scan(self):
        try:
            open_ports = self.port_scan()
            return {
                'open_ports': open_ports
            }
        except Exception as e:
            print(f"Active scan failed for {self.ip}: {str(e)}")

    def gather_entity_data(self, scan_type='passive'):
        ip_info = self.fetch_ip_geolocation()
        if scan_type == 'passive':
            return {
                'ip': self.ip,
                'reverse_dns': self.reverse_dns_lookup(),
                'ip_info': ip_info,
                'passive_scan_results': self.passive_scan(),
                'whois_info': self.whois_info(),
                'dns_records': self.dns_records()
            }
        elif scan_type == 'active':
            return {
                'ip': self.ip,
                'reverse_dns': self.reverse_dns_lookup(),
                'ip_info': ip_info,
                'active_scan_results': self.active_scan(),
                'whois_info': self.whois_info(),
                'dns_records': self.dns_records()
            }
        else:
            print("Invalid scan type. Please choose 'passive' or 'active'.")

    @staticmethod
    def display_entity_data(entity_data):
        return json.dumps(entity_data, indent=4)
