import socket
import sys
sys.path.insert(0, 'inter/modules')
import finder

web_server = '127.0.0.1'
server = socket.gethostbyname(socket.gethostname())
port = 3705
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', port))
    s.listen()
    while True:
        connection, address = s.accept()
        with connection:
            print(address)
            if address[0] == web_server:
                msg = None
                while True:
                    data = connection.recv(1024)
                    data = data.decode()
                    if data:
                        msg = data
                    else:
                        break
                print(msg)
                finder.respond_start(msg)
