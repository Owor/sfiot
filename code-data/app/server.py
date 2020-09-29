# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:47:41 2019
simple echo server only

@author: Darmawan Utomo
# -*- coding: utf-8 -*-
"""
#Created on Tue Apr 16 18:52:46 2019


import datetime
import time
import socket
import numpy as np



HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#HOST = '172.17.0.2'  # Standard loopback interface address (localhost)

PORT = 60005        # Port to listen on (non-privileged ports are > 1023)
##############CREATE INSTANCE RINGBUFFER SEBANYAK TIMESTEP
paket=''
while True:

    print("server is ready to receive CONNECTION and DATA ....")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data=''.encode()
            buf=''.encode()
            while True:
                data = conn.recv(1024)
                conn.sendall(data)

                if (b'806410004' in data):
                    print(data)
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                    break;
                    
