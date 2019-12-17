import socket
import sys
import os
import requests
from threading import Thread
import time
import argparse


def get_my_ip():
    return requests.get("http://eth0.me").text


def set_ip(port, login, password):
    while True:
        requests.post('https://perfect-elk.ru/api/setip/',{'user': login, 'pass': password, 'port': port, 'ip': get_my_ip()})
        time.sleep(60 * 60)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login')
    parser.add_argument('-p', '--password')
    parser.add_argument('-po', '--port', default=10995)
    namespace = parser.parse_args(sys.argv[1:])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "0.0.0.0"
    port = int(namespace.port)

    thread = Thread(target=set_ip, kwargs={'port': port, 'login': namespace.login, 'password': namespace.password}, name='set_ip')
    thread.start()

    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        data = conn.recv(1000000)
        if not os.path.exists(os.path.join(os.getcwd(), 'files')):
            os.makedirs(os.path.join(os.getcwd(), 'files'))
        _f = open(os.path.join(os.getcwd(),'files',str(data, 'UTF-8')), 'wb')
        _f.write(b'')
        _f.close()
        _f = open(os.path.join(os.getcwd(),'files',str(data, 'UTF-8')), 'ab')
        conn.send(b'1')
        while True:
            _data = conn.recv(1024 * 8)
            _f.write(_data)
            conn.send(b'1')
            if not _data:
                conn.send(b'1')
                break
        _f.close()

    conn.close()
