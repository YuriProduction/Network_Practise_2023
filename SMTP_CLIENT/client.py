import base64
import json
import os
import socket
import ssl
import mimetypes
import time

BUF_LEN = 1024
HOST_ADDR = 'smtp.yandex.ru'
PORT = 465


def request(s, req):
    s.send((req + '\n').encode())
    s.setblocking(0)
    recv_data = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            recv_data += chunk
            while len(recv_data) >= 4096:
                recv_data = recv_data[4096:]
        except socket.error as e:
            if e.errno == socket.errno.EWOULDBLOCK:
                print("No data available. Retrying...")
                time.sleep(1)
                continue
            else:
                print("Socket error:", e)
                break
    return recv_data


class SMTPClient:
    def __init__(self):
        self.attachments_path = None
        self.subject_msg = None
        self.arr_user_name_to = None
        self.user_name_from = None
        self.password = None
        self.ssl_contex = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_contex.check_hostname = False
        self.ssl_contex.verify_mode = ssl.CERT_NONE
        self.json_data_init()
        self.password_init()

    def message_prepare(self):
        with open('msg.txt') as file_msg:
            boundary_msg = "bound.40629"
            headers = f'from: {self.user_name_from}\n'
            users_name_to = ','.join(self.arr_user_name_to)
            headers += f'to: {users_name_to}\n'
            headers += f'subject: {self.subject_msg}\n'
            headers += 'MIME-Version: 1.0\n'
            headers += 'Content-Type: multipart/mixed;\n' \
                       f'\tboundary={boundary_msg}\n'

            message_body = f'--{boundary_msg}\n'
            message_body += 'Content-Type: text/plain; charset=utf-8\n\n'
            msg = file_msg.read()
            message_body += msg + '\n'
            message_body += f'--{boundary_msg}\n'

            for attachment in os.listdir(self.attachments_path):
                message_body += f'--{boundary_msg}\n'
                message_body += 'Content-Disposition: attachment;\n' \
                                f'\tfilename="{attachment}"\n'
                message_body += 'Content-Transfer-Encoding: base64\n'

                mime_type = mimetypes.guess_type(attachment)
                message_body += f'Content-Type: {mime_type[0]};\n\n'

                with open(self.attachments_path + '/' + attachment, 'rb') as attachment_file:
                    str_attachment = base64.b64encode(attachment_file.read()).decode()

                message_body += str_attachment + '\n'

            message_body += f'--{boundary_msg}--\n'

            message = headers + '\n' + message_body + '.\n'
            print(message)
            return message

    def json_data_init(self):
        with open('config.json', 'r') as json_file:
            file = json.load(json_file)
            self.user_name_from = file['from']  # считываем из конфига кто отправляет
            self.arr_user_name_to = file['to']  # считываем из конфига список кому отправляем
            if isinstance(self.arr_user_name_to, str):
                self.arr_user_name_to = [self.arr_user_name_to]
            self.subject_msg = file['subject']
            self.attachments_path = file['attachments_path']

    def password_init(self):
        with open("pswd.txt", "r", encoding="UTF-8") as file:
            self.password = file.read().strip()  # считываем пароль из файла

    def action(self):
        with socket.create_connection((HOST_ADDR, PORT)) as sock:
            with self.ssl_contex.wrap_socket(sock, server_hostname=HOST_ADDR) as client:
                print(client.recv(1024))  # в smpt сервер первый говорит
                print(request(client, f'ehlo {self.user_name_from}'))
                base64login = base64.b64encode(self.user_name_from.encode()).decode()

                base64password = base64.b64encode(self.password.encode()).decode()
                print(request(client, 'AUTH LOGIN'))
                print(request(client, base64login))
                print(request(client, base64password))
                print(request(client, f'MAIL FROM:{self.user_name_from}'))
                for user_name_to in self.arr_user_name_to:
                    print(request(client, f"RCPT TO:{user_name_to}"))
                print(request(client, 'DATA'))
                print(request(client, self.message_prepare()))


def main():
    smtp_client = SMTPClient()
    smtp_client.action()


if __name__ == '__main__':
    main()
