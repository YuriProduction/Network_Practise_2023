import socket
from dnslib import DNSRecord
import random

# Создаем сокет для клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Задаем адрес и порт сервера
server_address = ('localhost', 53)

# Список доменных имен для разрешения
domains = ['vk.com', 'ya.ru', 'amazon.com', 'openai.com', 'ya.ru']
types_queries = ['A', 'NS']

# Отправляем запросы на разрешение доменных имен
for domain in domains:
    # Отправляем запрос на сервер
    query_data = DNSRecord.question(domain, random.choice(types_queries)).pack()
    client_socket.sendto(query_data, server_address)

    # Получаем ответ от сервера
    resp_data, _ = client_socket.recvfrom(1024)
    resp = DNSRecord.parse(resp_data)

    # Выводим результат разрешения
    print(f"{resp}")

# Закрываем сокет клиента
client_socket.close()
