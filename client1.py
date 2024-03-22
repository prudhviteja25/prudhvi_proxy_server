import socket
host = 'localhost'
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
http_request = "GET http://example.com HTTP/1.1\r\nHost: example.com\r\n\r\n"
s.send(http_request.encode())

response = s.recv(1024)
while response:
    print("Received: " + response.decode())
    response = s.recv(1024)
s.close()