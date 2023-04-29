import socket

# Создаем сокет для клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Задаем адрес и порт сервера
server_address = ('localhost', 53)

# Список доменных имен для разрешения
domains = ['vk.com', 'ya.ru', 'amazon.com', 'openai.com', 'ya.ru']

# Отправляем запросы на разрешение доменных имен
for domain in domains:
    # Отправляем запрос на сервер
    client_socket.sendto(domain.encode(), server_address)

    # Получаем ответ от сервера
    ip, _ = client_socket.recvfrom(1024)

    # Выводим результат разрешения
    print(f"{domain} => {ip.decode()}")

# Закрываем сокет клиента
client_socket.close()
