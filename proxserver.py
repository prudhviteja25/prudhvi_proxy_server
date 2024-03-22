import socket
import ssl
import threading

def parse_request(request):
        
        lines = request.split("\n")
        host_line = next(line for line in lines if line.startswith("Host:"))
        return host_line.split(" ")[1].strip()



def handle_client(c):
    request=c.recv(1024)
    request_data = request.decode()
    print("received request",request_data)
    if("https" in request_data):
         dest_port=443
    else:
        dest_port=80
    dest_host= parse_request(request_data)
    dest_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(dest_port==443):
        dest_socket = ssl.wrap_socket(dest_socket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLS)


    dest_socket.connect((dest_host,dest_port))
    dest_socket.send(request_data.encode())
    response_data = dest_socket.recv(1024)
    #print(" Received response:", response_data.decode())
    c.send(response_data)
    dest_socket.close()
    c.close()


localhost="127.0.0.1"
port=8080
proxy_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    proxy_socket.bind((localhost,port))
    proxy_socket.listen(10)
    print("proxy server listening on","host:",localhost,"port:",port)
except Exception as e:
    print("error:",e)

while True:
    c,addr=proxy_socket.accept()
    print("ACCEPTED CONNECTION FROM ","host:",addr[0],"port:",addr[1])
    client_thread = threading.Thread(target=handle_client, args=(c,))
    client_thread.start()
    
