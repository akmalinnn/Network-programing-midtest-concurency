import os
import socket
import logging
import multiprocessing
import ssl
from http import HttpServer

httpserver = HttpServer()

class ProcessTheClient(multiprocessing.Process):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
        rcv = ""
        while True:
            try:
                data = self.connection.recv(32)
                if data:
                    d = data.decode()
                    rcv += d
                    if rcv[-4:] == '\r\n\r\n':
                        logging.info(f"Data from client: {rcv}")
                        hasil = httpserver.proses(rcv)
                        hasil = hasil + "\r\n\r\n".encode()
                        logging.info(f"Response to client: {hasil}")
                        self.connection.sendall(hasil)
                        rcv = ""
                        self.connection.close()
                        break
                else:
                    break
            except OSError as e:
                logging.error(f"OSError: {e}")
                break
        self.connection.close()

class Server(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.hostname = 'testing.net'
        cert_location = os.path.join(os.getcwd(), 'certs')
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(certfile=os.path.join(cert_location, 'domain.crt'),
                                     keyfile=os.path.join(cert_location, 'domain.key'))
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 8443))
        self.my_socket.listen(5)  # Increased backlog to handle more concurrent connections
        logging.info("Server started on port 8443")
        try:
            while True:
                connection, client_address = self.my_socket.accept()
                try:
                    secure_connection = self.context.wrap_socket(connection, server_side=True)
                    logging.info(f"Connection from {client_address}")
                    clt = ProcessTheClient(secure_connection, client_address)
                    clt.start()
                except ssl.SSLError as essl:
                    logging.error(f"SSL error: {essl}")
        finally:
            self.my_socket.close()

def main():
    logging.basicConfig(level=logging.INFO)
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
