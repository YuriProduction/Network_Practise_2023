import subprocess
import re
import json
from urllib import request
from table import TableManager
from dataVector import DataVector
from checks import Checks


def get_ip_info(ip):
    # преобразуем строку формата json в питоновский объект
    a = request.urlopen('https://ipinfo.io/' + ip + '/json').read()
    return json.loads(a)


def parse_ip(line):
    return re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)


def trace_as(address, table):
    # используем subprocess для запуска нового процесса в командной строке
    tracert_proc = subprocess.Popen(["tracert", address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    number = 0

    for raw_line in iter(tracert_proc.stdout.readline, ''):
        line = raw_line.decode('cp866')
        print('line: ', line, sep='\t')
        ip = parse_ip(line)

        if Checks.is_complete(line):
            print(table)
            return
        if Checks.is_invalid_input(line):
            print('invalid input')
            return
        if Checks.is_beginning(line):
            print(line)
            continue
        if Checks.is_timed_out(line):
            print('request timed out')
            continue
        if ip:
            print("ip: ", ip)
            number += 1
            info = get_ip_info(ip[0])
            print(info)
            if 'bogon' in info:
                table.add_row(DataVector().get_bogon_args(number, info))
            else:
                table.add_row(DataVector().get_args(number, info))


def main():
    address = input('Enter address: ')
    table = TableManager().generate_table()
    trace_as(address, table)


if __name__ == '__main__':
    main()
