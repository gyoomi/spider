#服务端
import socket

server = socket.socket()
server.bind(("0.0.0.0", 8000))
server.listen()

sock, addr = server.accept()

data = ""

while True:
    temp_data = sock.recv(1024)
    if temp_data:
        data += temp_data.decode("utf8")
    else:
        break

print(data)

server.close()
