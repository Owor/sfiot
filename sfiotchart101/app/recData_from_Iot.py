import socket, sys
import re
import threading
HOST_from_IoT = '127.0.0.1'  # LOCAL HOST
PORT_from_IoT = 60000        # The port IN LOCAL HOST

HOST_from_IoT = '127.0.0.1'  # LOCAL HOST
PORT_to_model = 60001        # The port IN LOCAL HOST
from socket_lib.socket_listen_for_inner import listen_inner_network_END
from socket_lib.client_for_inner import socket_connect_END 
import time
import numpy as np

#receive data 
#while(True):
   #rec_data = []
   #receive data from IoT_to_DNN.py
rec = listen_inner_network_END(PORT_from_IoT)
   #for i in rec:
   	   #把原本每筆資料尾巴的END去掉
   	   #i = i.strip(';END')
   	   #rec_data.append(i)
   
print(len(rec))
   

   #for j in rec:
   #	   print("receive data:",j)
   #print(len(rec))
   
   #傳資料給DNN model做 Anomaly detection
socket_connect_END(PORT_to_model, rec, len(rec))

   #time.sleep(2)

   #清空繼續接收 smart grid 資料
   #rec_data = []