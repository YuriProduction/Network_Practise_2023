import base64
import json
import os
import socket
import ssl
import mimetypes

BUF_LEN = 1024
host_addr = 'smtp.yandex.ru'
port = 465


def request(s, req):
    # s.send((req + '\n').encode())
    # s.settimeout(1)
    #
    # recv_data = ' '
    # try:
    #     while recv_data:
    #         recv_data += s.recv(BUF_LEN).decode()
    # except socket.timeout:
    #     pass
    #
    # return recv_data

    s.send((req + '\n').encode())
    recv_data = s.recv(65535).decode()  # надо в цикле
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
            headers += f'subject: {self.subject_msg}\n'  # короткая тема на латинице
            headers += 'MIME-Version: 1.0\n'
            headers += 'Content-Type: multipart/mixed;\n' \
                       f'\tboundary={boundary_msg}\n'

            # тело сообщения началось
            message_body = f'--{boundary_msg}\n'
            message_body += 'Content-Type: text/plain; charset=utf-8\n\n'
            msg = file_msg.read()
            message_body += msg + '\n'
            message_body += f'--{boundary_msg}\n'

            for attachment in os.listdir(self.attachments_path):
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
        with socket.create_connection((host_addr, port)) as sock:
            with self.ssl_contex.wrap_socket(sock, server_hostname=host_addr) as client:
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
                # print(request(client, 'QUIT'))


def main():
    smtp_client = SMTPClient()
    smtp_client.action()


if __name__ == '__main__':
    main()

