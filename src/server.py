import socket
import finder
web_server = '#'
port = #
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting up server on ({0}, {1})".format('#', port))
    s.bind(('#', port))
    s.listen()
    while True:
        connection, address = s.accept()
        with connection:
            print(address, "Connected")
            if address[0] == web_server:
                msg = None
                while True:
                    data = connection.recv(1024)
                    data = data.decode()
                    if data:
                        msg = data
                    else:
                        break
                print("Received", msg, "from", address)
                finder.respond_start(msg)
