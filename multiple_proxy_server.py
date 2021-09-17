
from client import get_remote_ip
import socket
import time
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 4096

def main():
    google_url = "www.google.com"
    google_port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as google_socket:
                google_ip = get_remote_ip(google_url)
                google_socket.connect((google_ip, google_port))
                p = Process(target=handle_proxy, args=(google_socket, conn))
                p.daemon = True
                p.start()
                print("Starting process", p)
            # delay just in case
            time.sleep(0.5)
            conn.close()

def handle_proxy(google_socket, proxy_conn):
    full_data = proxy_conn.recv(BUFFER_SIZE)
    google_socket.sendall(full_data)
    google_socket.shutdown(socket.SHUT_WR)
    data = google_socket.recv(BUFFER_SIZE)
    proxy_conn.send(data)

if __name__ == "__main__":
    main()