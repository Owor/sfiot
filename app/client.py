import time
from datetime import datetime
import socket


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000        # The port used by the server
KOLOM = 2
print('start establishing connection '+ HOST+ ':'+str(PORT)+'  and to send data ...')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(KOLOM):
        id = str(i)
        ts = str(datetime.now().timestamp())
        paket = id + ',' + ts + ',' +'END'
        print(paket)
        s.sendall(paket.encode())
        data = s.recv(1024)
        print('Received', repr(data))
        time.sleep(2)
    paket = '806410004'
    s.sendall(paket.encode())
    data = s.recv(1024)
    print('Received', repr(data))

