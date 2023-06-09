import socket
import datetime
from config_parser import parse_config_data


class SNTP_SERVER:
    def get_modified_time(self, offset):
        return datetime.datetime.now() + datetime.timedelta(seconds=offset)

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            delay, HOST, PORT = parse_config_data()
            print(HOST, PORT)
            server_socket.bind((HOST, PORT))
            while True:
                data, address = server_socket.recvfrom(1024)
                modified_time = self.get_modified_time(delay)
                formatted_time = modified_time.strftime("%Y-%m-%d %H:%M:%S")
                server_socket.sendto(str(formatted_time).encode(), address)


if __name__ == "__main__":
    sntp_server = SNTP_SERVER()
    sntp_server.run_server()
