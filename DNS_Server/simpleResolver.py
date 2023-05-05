import re
import socket


def is_valid_ip(ip_address):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip_address):
        return True
    else:
        return False


def domain_to_ip(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror:
        return "Не удалось разрешить IP-адрес"


def ip_to_domain(ip_address):
    try:
        domain_name = socket.gethostbyaddr(ip_address)[0]
        return domain_name
    except socket.herror:
        return "Не удалось разрешить доменное имя"




