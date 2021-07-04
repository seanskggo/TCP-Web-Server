# Python 3 (3.8.5) was used! 

import socket
import sys
import re
import os

def send_file(filename, conn, status):
    c_type = "image/png" if re.search(".png", filename) else "text/html"
    conn.send(f"HTTP/1.1 {status}\r\nContent-Type: {c_type}\r\n\r\n".encode())
    with open(filename, "rb") as file: 
        conn.send(file.read())
    print(f"GET {filename}")

if (len(sys.argv) != 2): exit("Wrong number of inputs!")
host, port = 'localhost', int(sys.argv[1])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
while True:
    conn, addr = server.accept()
    data = conn.recv(1024).decode()
    getter = re.search("GET /.* ", data)
    if getter: getter = getter.group().strip("GET /").strip()
    if getter == "": getter = "main.html"
    if not getter or getter not in [f for f in os.listdir('.') if os.path.isfile(f)]: 
        send_file("404.html", conn, "404 Not Found")
        continue
    send_file(getter, conn, "200 OK")
    conn.close()
