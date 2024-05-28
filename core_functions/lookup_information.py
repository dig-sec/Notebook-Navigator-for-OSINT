import socket
import whois
import requests

class NetworkEntityInformation:
    def __init__(self, ip):
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

    def gather_entity_data(self):
        ip_info = self.fetch_ip_geolocation()
        return {'ip': self.ip, 'ip_info': ip_info}

    @staticmethod
    def display_entity_data(entity_data):
        if entity_data:
            print(f"IP: {entity_data['ip']}")
            print(f"IP Info: {entity_data['ip_info']}")
        else:
            print("Failed to collect network entity information.")

class DomainInformation(NetworkEntityInformation):
    def __init__(self, domain):
        super().__init__(domain)
        self.domain = domain

    def fetch_dns_records(self, record_type='A'):
        try:
            records = socket.getaddrinfo(self.domain, None)
            record_list = [record[-1][0] for record in records if record[1] == socket.SOCK_STREAM]
            if not record_list:
                print(f"No {record_type} records found for {self.domain}")
            else:
                return record_list
        except socket.gaierror as e:
            if e.errno == socket.EAI_NONAME:
                print(f"No DNS record found for {self.domain}")
            else:
                print(f"Failed to get DNS records for {self.domain}: {str(e)}")

    def fetch_whois_data(self):
        try:
            whois_info = whois.whois(self.domain)
            if whois_info:
                return whois_info
            else:
                print(f"No WHOIS information found for {self.domain}")
        except Exception as e:
            print(f"Failed to get WHOIS info for {self.domain}: {str(e)}")

    def gather_domain_data(self):
        dns_records = self.fetch_dns_records()
        whois_info = self.fetch_whois_data()
        ip_info = self.fetch_ip_geolocation()
        return {'domain': self.domain, 'dns_records': dns_records, 'whois_info': whois_info, 'ip_info': ip_info}

    @staticmethod
    def display_domain_data(domain_data):
        if domain_data:
            print(f"Domain: {domain_data['domain']}")
            print(f"DNS Records: {domain_data['dns_records']}")
            print(f"WHOIS Info: {domain_data['whois_info']}")
            print(f"IP Info: {domain_data['ip_info']}")
        else:
            print("Failed to collect domain information.")

# Example usage:
entity = '192.0.2.0'  # replace with your IP address
domain = 'example.com'  # replace with your domain

network_info = NetworkEntityInformation(entity)
entity_data = network_info.gather_entity_data()
NetworkEntityInformation.display_entity_data(entity_data)

domain_info = DomainInformation(domain)
domain_data = domain_info.gather_domain_data()
DomainInformation.display_domain_data(domain_data)
