import socket, sys
import time
from pandas import read_csv

import sys
sys.path.append("../socket_lib")

from client_for_inner import socket_connect_END 
HOST = '127.0.0.1'  # LOCAL HOST
PORT = 60000        # The port IN LOCAL HOST
import time
 


#load meter dataset   
dataset = read_csv('Residential-Profiles_Plus_AVG_SORT.csv', header=0, index_col=0)
values = dataset.values
print(values.shape)
#print(values.type)


res = []
#在每筆資料加上Meter ID 和 END 然後傳給DNN_recData
for i in values[:200]:
   
   temp = i.tolist()
   for j,col in zip(range(len(temp)),dataset.columns):
      res.append(str(col) + ";" + str(temp[j])+";END")
   #localtime = time.asctime( time.localtime(time.time()) )
   #print("當下時間",localtime)
   #send data to rec_Data_from IoT (一次兩百筆，同一個時間點的meter資料)
   
   #time.sleep(5)
print(len(res))
socket_connect_END(PORT, res, len(res))

   
'''
#在每筆資料後面加END 傳出去
res = []
temp = values[0].tolist()
for i in range(len(temp)):
	res.append(str(temp[i])+";END")
socket_connect_END(PORT, res, len(res))
'''

