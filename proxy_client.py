from socket import socket
import client


HOST = ""
PORT = 8001
payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
buffer_size = 4096


def main():
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((HOST, PORT))

        #send the data and shutdown
        client.send_data(proxy_socket, payload.encode())
        proxy_socket.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        '''full_data = b""
        while True:
            data = proxy_socket.recv(buffer_size)
            if not data:
                break
            full_data += data'''
        full_data = proxy_socket.recv(buffer_size)
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        proxy_socket.close()

if __name__ == "__main__":
    main()