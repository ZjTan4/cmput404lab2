from socket import socket
import client
import time

HOST = ""
PORT = 8001
buffer_size = 4096

def main():
    google_url = "www.google.com"
    google_port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_socket.bind((HOST, PORT))
        #set to listening mode
        proxy_socket.listen(1)
        
        #continuously listen for connections
        while True:
            conn, addr = proxy_socket.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as google_socket:
                google_ip = client.get_remote_ip(google_url)
                google_socket.connect((google_ip, google_port))
                from_client = conn.recv(buffer_size)
                
                # forward
                google_socket.sendall(from_client)
                # send back
                data = google_socket.recv(buffer_size)

                conn.sendall(data)
            # delay
            time.sleep(0.5)
            #conn.sendall(bytes("hello", 'utf-8'))
            conn.close()

if __name__ == "__main__":
    main()