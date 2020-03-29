import socket

# http客户端

http_client = socket.socket()
http_client.connect(("www.baidu.com", 80))
http_client.send("GET / HTTP/1.1\r\n Connection: close\r\n\r\n".encode("utf8"))

data = ""
while True:
    temp_data = http_client.recv(2048)
    if temp_data:
        data += temp_data.decode("utf8")
    else:
        break


print(data)
