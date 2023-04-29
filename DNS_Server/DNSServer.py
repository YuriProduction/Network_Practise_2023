import socket
import pickle
import os
from datetime import datetime, timedelta

CACHE_FILE = 'cache.pickle'  # File name to store cache data
TTL_SECONDS = 3600  # TTL for cache entries (1 hour)


class DNSServer:
    def __init__(self):
        self.domain_to_ip = {}
        self.ip_to_domain = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as file:
                cache_data = pickle.load(file)
                if 'domain_to_ip' in cache_data and 'ip_to_domain' in cache_data:
                    self.domain_to_ip = cache_data['domain_to_ip']
                    self.ip_to_domain = cache_data['ip_to_domain']

    def save_cache(self):
        cache_data = {'domain_to_ip': self.domain_to_ip, 'ip_to_domain': self.ip_to_domain}
        with open(CACHE_FILE, 'wb') as file:
            pickle.dump(cache_data, file)

    def resolve(self, domain):
        if domain in self.domain_to_ip:
            ip_address = self.domain_to_ip[domain]
            if ip_address in self.ip_to_domain:
                self.ip_to_domain[ip_address] = datetime.now()  # Update the timestamp for IP-to-domain mapping
            return ip_address
        else:
            # Perform your DNS resolution logic here to obtain the IP address for the domain
            ip_address = self.dns_resolve(domain)  # Replace with your DNS resolution function
            self.domain_to_ip[domain] = ip_address
            self.ip_to_domain[ip_address] = datetime.now()
            self.save_cache()  # Save cache data after adding a new entry
            return ip_address

    def dns_resolve(self, domain):
        # Implement your DNS resolution logic here
        # Return the IP address corresponding to the given domain
        # This function should handle the actual DNS resolution process, such as querying external DNS servers
        # Replace this placeholder implementation with your own implementation
        return socket.gethostbyname(domain)

    def remove_expired_entries(self):
        now = datetime.now()
        expired_ips = [ip for ip, timestamp in self.ip_to_domain.items() if
                       now - timestamp >= timedelta(seconds=TTL_SECONDS)]
        for ip in expired_ips:
            del self.ip_to_domain[ip]
            domains_to_remove = [domain for domain, ip_address in self.domain_to_ip.items() if ip_address == ip]
            for domain in domains_to_remove:
                del self.domain_to_ip[domain]

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('localhost', 53))

        print("DNS Server started.")

        while True:
            data, addr = server_socket.recvfrom(1024)
            domain = data.decode().strip()

            if domain == 'exit':
                break

            ip_address = self.resolve(domain)
            server_socket.sendto(ip_address.encode(), addr)

            self.remove_expired_entries()  # Remove expired cache entries after each request

        server_socket.close()


dns_server = DNSServer()
dns_server.run()
