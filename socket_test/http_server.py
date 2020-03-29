import socket
import threading

# socket服务端

server = socket.socket()
server.bind(("0.0.0.0", 8000))
server.listen()


def handle_sock(sock, addr):
    while True:
        temp_data = sock.recv(1024)
        print(temp_data.decode("utf8"))
        response_template = ''' HTTP/1.1 200 OK

        <html>
            <body>
                <h1>hello, this is python http server</h1>
            </body>
        </html>
        '''
        sock.send(response_template.encode("utf8"))


while True:
    sock, addr = server.accept()
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()

