import argparse
import threading
import socket


def check_tcp_port(address, port, mode):
    with socket.socket(socket.AF_INET, mode) as sock:
        sock.settimeout(0.3)
        try:
            sock.connect((address, port))
            print('Tcp PORT ' + str(port) + ' is open!')
            sock.close()
        except:
            pass


def check_udp_port(address, port):
    socket.setdefaulttimeout(3)
    Message = b'Hello,world!'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.sendto(Message, (address, port))
            data, _ = sock.recvfrom(1024)
            print(data)
            if data.decode('utf-8') != 'порт недоступен':
                print(f'Udp {port} is open')
        except socket.error:
            pass


def create_and_start_list_of_processes(*args):
    threads_for_tcp = [threading.Thread(target=check_tcp_port, args=[args[0], port, socket.SOCK_STREAM], daemon=False)
                       for port in range(args[1], args[2] + 1)]
    threads_for_udp = [threading.Thread(target=check_udp_port, args=[args[0], port], daemon=False)
                       for port in range(args[1], args[2] + 1)]
    [th.start() for th in threads_for_tcp]
    [th.start() for th in threads_for_udp]
    [th.join() for th in threads_for_tcp]
    [th.join() for th in threads_for_udp]


def parse_arguments() -> tuple:
    parser = argparse.ArgumentParser()
    parser.add_argument('address', type=str, help='ip or domain name')
    parser.add_argument('left_boundary', type=int, help='left border')
    parser.add_argument('right_boundary', type=int, help='right border')
    args = parser.parse_args()

    return args.address, args.left_boundary, args.right_boundary


def main_func():
    address, left_boundary, right_boundary = parse_arguments()
    create_and_start_list_of_processes(address, left_boundary, right_boundary)


main_func()
