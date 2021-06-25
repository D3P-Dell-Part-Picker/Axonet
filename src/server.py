import socket
import finder

web_server = '10.12.33.212'
port = 3705
# start up a server to receive message from the web server and find the locations and light up locations
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Starting up server on ({0}, {1})".format('10.12.33.231', port))
    s.bind(('10.12.33.231', port))
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
                connection.shutdown(0)
                connection.close()
