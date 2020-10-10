 # -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:47:41 2019

@author: Darmawan Utomo
PORT 60000
"""

# -*- coding: utf-8 -*-
"""
DNN CLIENT-SIMULATOR
Created on Tue Apr 16 18:50:26 2019

@author: TK1
"""

LIMIT_SZIE = 200
time_block = 5
import time
from datetime import datetime
import socket
from pandas import read_csv
from pandas import DataFrame
from pandas import concat

import sys
sys.path.append("../socket_lib")

from socket_listen_for_inner import listen_inner_network_END
HOST_from_IoT = '127.0.0.1'  # LOCAL HOST
PORT_from_IoT = 10000        # The port IN LOCAL HOST
import numpy as np
#=====================================================================================
# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
   n_vars = 1 if type(data) is list else data.shape[1]
   df = DataFrame(data)
   cols, names = list(), list()
   # input sequence (t-n, ... t-1)
   for i in range(n_in, 0, -1):
    cols.append(df.shift(i))
    names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
   # forecast sequence (t, t+1, ... t+n)
   for i in range(0, n_out):
    cols.append(df.shift(-i))
    if i == 0:
     names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
    else:
     names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
   # put it all together
   agg = concat(cols, axis=1)
   agg.columns = names
   # drop rows with NaN values
   if dropnan:
    agg.dropna(inplace=True)
   return agg
#========================================================================================
#received_data = []
#while(True):
#received_data = listen_inner_network_END(PORT_from_IoT)
#print("==================================================================================")
#print(len(received_data))
 #received_data.append(rec)

#   when already received 200 Meter * 200 timestamp data |   total = 200*200 = 40000
 #if len(received_data) >= 40000:
 # break
# break



meter_sort_list = [""]*200
temp_200_meter_consumtion = [""]*200
temp_40000_meter_consumtion = []
count=0
#show the sort_list data
#for i in 200_meter_sort_list:
# print(i)
#

#========================================= 一次收40000筆的版本after sort meter id===================================
meter_sort_list = [""]*200
received_data = listen_inner_network_END(PORT_from_IoT)#一次收40000筆
for i in received_data:
   temp = i.split(';')
   time_step = temp[1].split('2020-05-21,12:58:')[1]
   meter_sort_list[int(temp[0].split('H-')[1])-1] = received_data   # temp[0].split('H-')[1] is meter id
   temp_200_meter_consumtion[int(temp[0].split('H-')[1])-1] = temp[3]  #temp[3] is meter consumtion
   count+=1

   #處理完meter id 排序 和 取出 consumtion後
   #每收集200個consumtion 就傳給model
   if count == 200: 
    print("time step "+ time_step + " data")
    print("200 meter consumtion :　",temp_200_meter_consumtion)


    #收集到200個meter資料後
    for i in temp_200_meter_consumtion:
     temp_40000_meter_consumtion.append(i)

    #clear temp_200_meter_consumtion for next collection
    temp_200_meter_consumtion = [""]*200
    count=0


   #收集到40000筆資料後做第一次預測
   if len(temp_40000_meter_consumtion) == 40000:
    #轉成200*200當作model第一次輸入
    input_data__arr = np.reshape(temp_40000_meter_consumtion,(200,200))
    values = input_data__arr.astype('float32')
    scaled = values/max(map(max,values)) 
    reframed = series_to_supervised(scaled, 1, 1)
    values = reframed.values

    print("==============================")
    print("正規劃後格式:",values.shape)
    print("==============================")
    print("正規劃後資料:",values)
    print("==============================")
    n_train_hours = 160
    n_test_hours = 40

    #BATCHSIZE=250
    INTERVAL = 200
    NUM_OF_COLOMNS = 200
    TIMESTEP=200

    test = values[n_train_hours:n_train_hours+n_test_hours,::]


    # split into input and outputs and arrange to consider INTERVAL
    tsx, tsy = test[:, :200], test[:, 200:400] # kolom 0-199 dgn GT:200-399
    print("========================")
    print("tsx:",tsx)
    print("========================")


    HOST = '127.0.0.1'  # LOCAL HOST
    PORT_to_DNN_SERVER = 60001        # The port IN LOCAL HOST
    KOLOM=200
    current=0

    data = np.zeros((200,KOLOM))
    dt = np.dtype([('ID', np.unicode_, 16), ('TIMESTAMP', 'datetime64[m]'),('USAGE',np.float64),('STATUS',np.str,8)])
    x = np.array([(199, '1979-03-22T15:00', 34.56, 'BLANK')], dtype=dt)
    jmlROW = 250
    dt = np.dtype([('ID', np.int64), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,8)])
    print('start establishing connection and to send data ...', HOST, PORT_to_DNN_SERVER)
    x = np.zeros((200), dtype=dt) #creating array of new datatype
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT_to_DNN_SERVER))
     for iFILL_MAX in range(jmlROW+1):
      for i in range(KOLOM):
       id = str(i)
       ts = str(datetime.now().timestamp())
       usg = str(tsx[iFILL_MAX][i])
       paket = id + ',' + ts + ','+ usg + ',' +'END'
       print(paket)
       s.sendall(paket.encode())
       data = s.recv(1024)
       print('Received', repr(data))

      s.sendall('123Xcq'.encode()) #send code setelah 200 kali kirim
     s.sendall('806410004'.encode()) #send EXIT code   








#========================================= 一次收40000筆的版本after sort meter id===================================




#========================================= 一次收一筆的版本after sort meter id===================================
'''
while(True):
 time_step = ""
 received_data = listen_inner_network_END(PORT_from_IoT)
 
 print("receive successful : " , received_data)

 temp = received_data[0].split(';') 
 time_step = temp[1].split('2019-12-05,00:00:')[1]
 meter_sort_list[int(temp[0].split('H-')[1])-1] = received_data[0]   # temp[0].split('H-')[1] is meter id
 temp_200_meter_consumtion[int(temp[0].split('H-')[1])-1] = temp[3]  #temp[3] is meter consumtion
 count+=1



 #處理完meter id 排序 和 取出 consumtion後
 #每收集200個consumtion 就傳給model
 if count == 200: 
  print("time step "+ time_step + " data")
  print("200 meter consumtion :　",temp_200_meter_consumtion)


  #收集到200個meter資料後
  for i in temp_200_meter_consumtion:
   temp_40000_meter_consumtion.append(i)

  #clear temp_200_meter_consumtion for next collection
  temp_200_meter_consumtion = [""]*200
  count=0

 #收集到40000筆資料後做第一次預測
 if len(temp_40000_meter_consumtion) == 40000:
  #轉成200*200當作model第一次輸入
  input_data__arr = np.reshape(temp_40000_meter_consumtion,(200,200))
  values = input_data__arr.astype('float32')
  scaled = values/max(map(max,values)) 
  reframed = series_to_supervised(scaled, 1, 1)
  values = reframed.values


 




'''
#=========================================after sort meter id===================================
'''
time = 200
rec_data = []
flag = 0
#receive data 
while(True):
 #harry modify
 print(len(received_data))
 for index, a_meter_data in enumerate(received_data):
  temp = a_meter_data.split(';') 
  if temp[3] == "":
   print("row = "+ str(index / 200))
   print("col = "+ str(index % 200))
   break
  rec_data.append(temp[3])  #Only take consumption data
 flag = 1

 #每兩百個時間點資料就傳給SERVER
 if (flag == 1) :
  rec_data_arr = np.reshape(rec_data,(time,200))
  print("筆資料格式（time,200）",rec_data_arr.shape)
  #rec.clear()
  values = rec_data_arr.astype('float32')
  scaled = values/max(map(max,values)) 
  reframed = series_to_supervised(scaled, 1, 1)
  values = reframed.values
  print("==============================")
  print("正規劃後格式:",values.shape)
  print("==============================")
  print("正規劃後資料:",values)
  print("==============================")
  n_train_hours = 160
  n_test_hours = 40

  #BATCHSIZE=250
  INTERVAL = 200
  NUM_OF_COLOMNS = 200
  TIMESTEP=200

  test = values[n_train_hours:n_train_hours+n_test_hours,::]


  # split into input and outputs and arrange to consider INTERVAL
  tsx, tsy = test[:, :200], test[:, 200:400] # kolom 0-199 dgn GT:200-399
  print("========================")
  print("tsx:",tsx)
  print("========================")


  HOST = '127.0.0.1'  # LOCAL HOST
  PORT_to_DNN_SERVER = 6000        # The port IN LOCAL HOST
  KOLOM=200
  current=0

  data = np.zeros((200,KOLOM))
  dt = np.dtype([('ID', np.unicode_, 16), ('TIMESTAMP', 'datetime64[m]'),('USAGE',np.float64),('STATUS',np.str,8)])
  x = np.array([(199, '1979-03-22T15:00', 34.56, 'BLANK')], dtype=dt)
  jmlROW = 250
  dt = np.dtype([('ID', np.int64), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,8)])
  print('start establishing connection and to send data ...', HOST, PORT_to_DNN_SERVER)
  x = np.zeros((200), dtype=dt) #creating array of new datatype
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   s.connect((HOST, PORT_to_DNN_SERVER))
   for iFILL_MAX in range(jmlROW+1):
    for i in range(KOLOM):
     id = str(i)
     ts = str(datetime.now().timestamp())
     usg = str(tsx[iFILL_MAX][i])
     paket = id + ',' + ts + ','+ usg + ',' +'END'
     print(paket)
     s.sendall(paket.encode())
     data = s.recv(1024)
     print('Received', repr(data))

    s.sendall('123Xcq'.encode()) #send code setelah 200 kali kirim
   s.sendall('806410004'.encode()) #send EXIT code   
'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
                
                 
                    
                   
                
            
  


 

'''    
# now rec_data is list(len=400)
#print("before reshape:",rec_data)
#print("before reshape",rec_data.shape)

rec_data_arr = np.reshape(rec_data,(time,200))
#now x is ndarray(2,200) from rec_data
#print("after reshape:",rec_data_arr)
#print("after reshape",rec_data_arr.shape)

#######==========================Arthur test area==========================


values = rec_data_arr.astype('float32')

scaled = values/max(map(max,values)) #to normalize data to the max values
# frame as supervised learning (scaled,1,jumlah next timesteps ts+2) kolom bengkak
reframed = series_to_supervised(scaled, 1, 1)

 '''
