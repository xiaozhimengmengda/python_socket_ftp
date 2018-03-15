import socketserver
import logging
import threading
import os


FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class FtpServer(socketserver.BaseRequestHandler):
    def setup(self):
        super().setup()
        self.event = threading.Event()

    def finish(self):
        super().finish()
        self.event.set()

    def handle(self):
        super().handle()
        while not self.event.is_set():
            logging.info("{}-{}-{}".format(self.request, self.client_address, self.server))
            data = self.request.recv(1024).decode().strip("")
            data = data.split("|")
            method = data[0]
            if method == "put":
                method, filename, filename_size = data
                msg = "ready".encode()
                self.request.send(msg)
                self.put(filename, filename_size)
            elif method == "get":
                msg = "down"
                filename_size = self.get_filename_size(filename)
                if filename_size != "error":
                    print(msg, filename, filename_size)
                    self.request.send("{}|{}|{}".format(msg, filename, filename_size).encode(encoding="utf-8"))
                    self.get(filename, filename_size)
                else:
                    self.request.send("file not exits".encode(encoding="utf-8"))
            else:
                pass

    def put(self, filename, filename_size):
        with open(filename, "wb") as f:
            recv_size = 0
            flag = True
            data = 0
            while flag:
                if recv_size < int(filename_size):
                    data = self.request.recv(1024)
                    recv_size += len(data)
                else:
                    recv_size = 0
                    flag = False
                    continue
                f.write(data)
        logging.info("upload success")

    def get(self, filename, filename_size):
        with open(filename, "rb") as f:
            send_size = 0
            flag = True
            data = 0
            while flag:
                if send_size + 1024 > filename_size:
                    data = f.read(filename_size - send_size)
                    flag = False
                else:
                    data = f.read(1024)
                    send_size += 1024
                self.request.send(data)
        logging.info("download success")

    def get_filename_size(self, filename):
        if os.path.isfile(filename):
            file_size = os.path.getsize(filename)
            return file_size
        return "error"


if __name__ == '__main__':
    addr = ("0.0.0.0", 9999)
    server = socketserver.ThreadingTCPServer(addr, FtpServer)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()








