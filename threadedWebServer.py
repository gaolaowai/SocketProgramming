import socket
import sys
from _thread import *
import time

#host = str(socket.gethostbyname(socket.gethostname()))
host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))

except socket.error as e:
    print("ERRRORRRR", str(e))
    

s.listen(10000)

def threaded_client(conn):
    #conn.send(str.encode("Welcome, type your name:\n"))
#    while True:
    #data = conn.recv(2048)
    #reply = "Server output: {}".format(data.decode())
    #reply = "HTTP/1.1 200 OK\nDate: {}\nServer: Simple-Python-HTTP-Server\nConnection: close".format((time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())),)

    reply = """HTTP/1.1 403 Forbidden
Date: Sun, 18 Oct 2009 11:58:41 GMT
Server: Apache/2.2.14 (Win32)
Content-Length: 222
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n
<html><head>\n
<title>403 Forbidden</title>\n
</head><body>\n
<h1>Forbidden</h1>\n
<p>You don't have permission to access /forbidden/index.html on this server.\n</p>
</body></html>\n"""
    conn.sendall(str.encode(reply))
    conn.close()

while True:
    
      
    conn, addr = s.accept()
    #print("Connected to: {}:{}\nConnection: {}".format(addr[0], addr[1], conn))
    #print(conn.recv(4098).decode())
    start_new_thread(threaded_client, (conn,))
