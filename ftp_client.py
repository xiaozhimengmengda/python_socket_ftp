import logging
import os
from socket import AF_INET, SOCK_STREAM, socket


FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


HOST = '192.168.33.10'
PORT = 9999
BUFSIZ = 1024
ADDR = (HOST, PORT)


class Ftp_Client:
    def __init__(self,host, port, bufsize, addr):
        self.host = host
        self.port = port
        self.bufsize = bufsize
        self.addr = addr

    def put(self):
        pass

    def get(self):
        pass

    def get_filename_size(self):
        pass


tcp_client = socket(AF_INET, SOCK_STREAM)
tcp_client.connect(ADDR)
while True:
    data = input(">")
    data = data.split(" ")
    method, filename = data

    if method == "put":
        if os.path.isfile(filename):
            filename_size = os.path.getsize(data[1])
            tcp_client.send("{}|{}|{}".format(method, filename, filename_size).encode(encoding="utf-8"))
            data = tcp_client.recv(BUFSIZ)
            data = data.decode()
            if data == "ready":
                logging.info("{}{} upload".format(filename, data))
                send_size = 0
                flag = True
                with open(filename, 'rb') as f:
                    while flag:
                        if send_size + 1024 > filename_size:
                            send_data = f.read(filename_size-send_size)
                            flag = False
                        else:
                            send_data = f.read(1024)
                            send_size += 1024
                        tcp_client.send(send_data)
                logging.info("upload success")

    elif method == "get":
        tcp_client.send("{}|{}".format(method, filename).encode(encoding="utf-8"))
        data = tcp_client.recv(BUFSIZ)
        data = data.decode()
        data = data.split("|")
        print(data)
        if len(data) > 2:
            msg, filename, filename_size = data
            if msg == "down":
                logging.info("{} down".format(filename))
                recv_size = 0
                flag = True
                with open("5431.txt", 'wb') as f:
                    while flag:
                        if int(filename_size) - recv_size > 1024:
                            recv_data = tcp_client.recv(1024)
                            recv_size += len(recv_size)
                        else:
                            recv_data = tcp_client.recv(int(filename_size)-recv_size)
                            recv_size += int(filename_size)-recv_size
                            flag = False
                        f.write(recv_data)
                logging.info("down success")
        else:
            print(tcp_client.recv(1024).decode())





tcp_client.close()

# with socket(AF_INET, SOCK_STREAM) as tcp_client:
#     tcp_client.connect(ADDR)
#     data = input(">")
#     tcp_client.send(data.encode("utf-8"))
#     data = tcp_client.recv(BUFSIZ)
#     print('Received', repr(data))
