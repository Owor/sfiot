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

import time, sys
from datetime import datetime
import socket
from pandas import read_csv
from pandas import DataFrame
from pandas import concat

import numpy as np
sys.path.append("../socket_lib")

from socket_listen_for_inner import *


data_set = listen_inner_network(6000)

# load dataset
# dataset = read_csv('Residential-Profiles_Plus_AVG_SORT.csv', header=0, index_col=0)
values = dataset.values
# integer encode direction
#encoder = LabelEncoder()
#values[:,0] = encoder.fit_transform(values[:,0])
# ensure all data is float
values = values.astype('float32')
# normalize features
#nomalisasi per kolom, bukan secara keseluruhan
##scaler = MinMaxScaler(feature_range=(0, 1))
##scaled = scaler.fit_transform(values)
scaled = values/max(map(max,values)) #to normalize data to the max values
# frame as supervised learning (scaled,1,jumlah next timesteps ts+2) kolom bengkak
reframed = series_to_supervised(scaled, 1, 1)
# drop columns we don't want to predict
#reframed.drop(reframed.columns[[9,10,11,12,13,14,15]], axis=1, inplace=True)
#print(reframed.head())
 
# split into train and test sets

values = reframed.values
n_train_hours = 40000
n_test_hours = 10000


#BATCHSIZE=250
INTERVAL = 200


NUM_OF_COLOMNS = 200
TIMESTEP=200
test = values[n_train_hours:n_train_hours+n_test_hours,::]

# split into input and outputs and arrange to consider INTERVAL
tsx, tsy = test[:, :200], test[:, 200:400] # kolom 0-199 dgn GT:200-399


HOST = '127.0.0.1'  # LOCAL HOST
PORT = 65432        # The port IN LOCAL HOST

##############CREATE INSTANCE RINGBUFFER SEBANYAK TIMESTEP
KOLOM=200
current=0
data = np.zeros((200,KOLOM))
dt = np.dtype([('ID', np.unicode_, 16), ('TIMESTAMP', 'datetime64[m]'),('USAGE',np.float64),('STATUS',np.str,8)])
x = np.array([(199, '1979-03-22T15:00', 34.56, 'BLANK')], dtype=dt)

jmlROW = 250
#############READ ONE ROW, SPLIT INTO KOLOM-200


dt = np.dtype([('ID', np.int64), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,8)])
x = np.zeros((200), dtype=dt) #creating array of new datatype
print('start establishing connection and to send data ...', HOST, PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for iFILL_MAX in range(jmlROW+1):
        for i in range(KOLOM):
            id = str(i)
            ts = str(datetime.now().timestamp())
            usg = str(tsx[iFILL_MAX][i])
            paket = id + ',' + ts + ','+ usg + ',' +'END'
            print(paket)
            s.sendall(paket.encode())
            #s.sendall('END'.encode())
            data = s.recv(1024)
            print('Received', repr(data))
            #strdata = str(data)[2:-1] #to remove the 'b   '
            #dw = strdata.split(',')
            #x[i][0] = int(dw[0])
            #x[i][1] = float(dw[1])
            #x[i][2] = float(dw[2])
            #x[i][3] = dw[3]
            
            #strdata = str(data).split(',')

        s.sendall('123Xcq'.encode()) #send code setelah 200 kali kirim
    s.sendall('806410004'.encode()) #send EXIT code


#datetime.datetime.now().timestamp()
#Out[33]: 1555424796.230251
#datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S')
#Out[34]: '2019-04-16 22:28:08'
