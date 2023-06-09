import socket
from config_parser import parse_config_data


def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            _, HOST, PORT = parse_config_data()
            client_socket.sendto(b"Time Request", (HOST, PORT))
            data, _ = client_socket.recvfrom(1024)
            print(f"Real time: {data.decode()}")


if __name__ == "__main__":
    run_client()
