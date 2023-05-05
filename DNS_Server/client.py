import socket
from dnslib import DNSRecord
import random
import simpleResolver

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 53)

domains = ['google.com', 'amazon.com', 'ya.ru', '8.8.8.8', 'vk.com']
record_types = ['A', 'NS']

for domain in domains:
    print('__________________________________')
    if simpleResolver.is_valid_ip(domain):
        print(domain + ' ' + simpleResolver.ip_to_domain(domain))
    else:
        print(domain + ' ' + simpleResolver.domain_to_ip(domain))
    query_data = DNSRecord.question(domain, random.choice(record_types)).pack()
    print('__________________________________')
    client_socket.sendto(query_data, server_address)

    resp_data, _ = client_socket.recvfrom(1024)
    resp = DNSRecord.parse(resp_data)

    print(f"{resp}")

client_socket.close()
