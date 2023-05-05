import os
import pickle
import socket
from datetime import datetime, timedelta
import re
from dnslib import DNSRecord, RCODE

CACHE_FILE = 'cache.pickle'
TTL_SECONDS = 10


class DNSServer:
    def __init__(self):
        self.cache = {}
        self.load_cache()

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as file:
                cache_data = pickle.load(file)
                for key, (record, expiry) in cache_data.items():
                    if datetime.now() - expiry < timedelta(seconds=TTL_SECONDS):
                        self.cache[key] = (record, expiry)

    def save_cache(self):
        with open(CACHE_FILE, 'wb') as file:
            pickle.dump(self.cache, file)

    def get_record_from_cache(self, key):
        record_data = self.cache.get(key)
        if record_data:
            record, expiry = record_data
            return record
        return None

    def resolve(self, query_data):
        try:
            query = DNSRecord.parse(query_data)
            # берем из кэша
            cached_record = self.get_record_from_cache((query.q.qname, query.a.rtype))
            # удалось - возвращаем
            if cached_record:
                return cached_record.pack()

            # DNS яндекса
            response = query.send('77.88.8.1', 53)
            response_record = DNSRecord.parse(response)

            if response_record.header.rcode == RCODE.NOERROR:
                self.update_cache(response_record.a.rname, response_record)
                self.save_cache()

            return response
        except Exception as error:
            print(f"Error: {error}")
            return None

    def ip_to_domain(self, ip_address):
        try:
            domain_name = socket.gethostbyaddr(ip_address)[0]
            return domain_name
        except socket.herror:
            return "Не удалось разрешить доменное имя"

    def is_valid_ip(self, ip_address):
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(pattern, ip_address):
            return True
        else:
            return False

    def domain_to_ip(self, domain_name):
        try:
            ip_address = socket.gethostbyname(domain_name)
            return ip_address
        except socket.gaierror:
            return "Не удалось разрешить IP-адрес"

    def remove_expired_entries(self):
        now = datetime.now()
        expired_ips = [record for record, timestamp in self.cache.items() if
                       now - timestamp[1] >= timedelta(seconds=TTL_SECONDS)]
        for record in expired_ips:
            del self.cache[record]

    def update_cache(self, key, record):
        # сохраняем как ключ еще и тип записи
        self.cache[(key, record.a.rtype)] = (record, datetime.now())

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('localhost', 53))

        print("DNS Server started.")

        try:
            while True:
                query_data, addr = server_socket.recvfrom(1024)
                resp_data = self.resolve(query_data)

                if resp_data:
                    server_socket.sendto(resp_data, addr)

                self.remove_expired_entries()  # Remove expired cache entries after each request
        except KeyboardInterrupt:
            print('Interrupted. DNS server is switching of...')
            server_socket.close()


dns_server = DNSServer()
dns_server.run()
