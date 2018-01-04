import socket
import sys
from _thread import *

host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))

except socket.error as e:
    print(str(e))

s.listen(5)

def threaded_client(conn):
    conn.send(str.encode("Welcome, type your name:\n"))

    while True:
        data = conn.recv(2048)
        reply = "Server output: {}".format(data.decode())
        if not data:
            break
        conn.sendall(str.encode(reply))
    conn.close()

while True:
    
      
    conn, addr = s.accept()
    print("Connected to: {}:{}\nConnection: {}".format(addr[0], addr[1], conn))
    print(conn.recv(4098).decode())

    start_new_thread(threaded_client, (conn,))
