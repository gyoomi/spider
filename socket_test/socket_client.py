import socket

# 客户端
client = socket.socket()
client.connect(("127.0.0.1", 8000))
client.send("哈哈".encode("utf8"))
client.close()

