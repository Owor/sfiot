# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:47:41 2019

@author: Darmawan Utomo
# -*- coding: utf-8 -*-
DtTm.datetime.fromtimestamp(int(float(ts)))
Out[13]: datetime.datetime(2019, 9, 2, 9, 47, 23)

print(str(ts[0])+','+str(DtTm.datetime.fromtimestamp(ts[1]).strftime('%Y-%m-%d %H:%M:%S'))+',' \
          +str(ts[2])+','+str(ts[3]),end=' ')
"""
#Created on Tue Apr 16 18:52:46 2019


import datetime as DtTm
import time
import socket
import numpy as np
from keras.models import model_from_json





NO = '_ALL'
# load json and fill model
json_file = open("DNN_model"+ NO +".json", 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("DNN_Grp"+ NO +".h5")
print("Loaded model-" + NO + " and weight from disk")


model.summary() #or for layer in model.layers: print(layer.output_shape)


#INTERVAL = 200 = TIMESTEP
#current=0


#datetime.datetime.now().timestamp()
#Out[33]: 1555424796.230251
#datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S')
#Out[34]: '2019-04-16 22:28:08'
def prtTimeStamp(ts):
    print(str(ts[0])+','+str(DtTm.datetime.fromtimestamp(ts[1]).strftime('%Y-%m-%d %H:%M:%S'))+',' \
          +str(ts[2])+','+str(ts[3]),end=' ')


TIMESTEP=200
KOLOM=200
#dt = np.dtype([('ID', np.unicode_, 16), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,8)])
dt = np.dtype([('ID', np.int64), ('TIMESTAMP', np.float64),('USAGE',np.float64),('STATUS',np.str,8)])
ts_data = np.zeros((200), dtype=dt) #creating array of new datatype
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
strdata=''
dw=''
##############CREATE INSTANCE RINGBUFFER SEBANYAK TIMESTEP

data4DNNin = np.zeros((200,KOLOM))
ccc = np.zeros((1,KOLOM)) # to get the USAGE DATA FROM TS-data
j=0 # to fill the TIMESTEP UPTO 200 AFTER THAT CHANGE TO DELETE-APPEND
i=0
ii=0
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
            #TO EXIT FROM SERVER PROGRAM
            if (b'806410004' in data):
                break
            #200 DATA FROM SMARTMETERS HAVE BEEN COLLECTED -> READY TO
            #FIRE THE INFERENCE ENGINE    
            if ( b'123Xcq' in data):
                data=''.encode()
                buf=''.encode()
                #for i in range(200):
                #    print(ts_data[i])
                #TEST THE ANOMALY
#==============================================================================
# BLOCK IF WE WANT START INFERENCING AFTER 200 ROWS OF DATA OR 1 TIMESTEP
#                if (j < TIMESTEP) : 
#                    for i in range(KOLOM): #copy from TS-DATA,USAGE ONLY
#                        ccc[0,i] = ts_data[i][2]
#                    data4DNNin[j] = ccc[0] # move to BLOCK TIMESTEPS
#                    j = j+1 #TO PROTECT SO THAT THE BUFFER MAXIMUM 200TSs
#                    print('REACH : ', j-1)
#                if (j == 200) : 
#                    print('BLOCK IS FULL, ready to INFER')
#                
#                if (j >= TIMESTEP):
#                    for i in range(KOLOM):
#                        ccc[0,i] = ts_data[i][2]
#                    data4DNNin= np.delete(data4DNNin, (0),axis=0)
#                    data4DNNin= np.append(data4DNNin, ccc,axis=0)
#                    print('INFER using DNN',j)
#                    j = j+1
                #=======================================================
                #GENERAL WAY, GET 1 ROW OF DATA->SLIDING->INFER
                for i in range(KOLOM):
                    ccc[0,i] = ts_data[i][2]
                data4DNNin= np.delete(data4DNNin, (0),axis=0)
                data4DNNin= np.append(data4DNNin, ccc,axis=0)
                #print('INFER using DNN',j)
                
                
                #INFERENCING
                prediction_results = model.predict(data4DNNin.reshape(1,200,200), verbose=0)
                #UPDATE THE STATUS
                for i in range(KOLOM): #copy from TS-DATA,USAGE ONLY
                    ts_data[i][3] = prediction_results[0,i]
                
                #SEND TO THE BLOCK CHAIN
                
                if (j >= 200) :
                    print(j,end=' '); prtTimeStamp(ts_data[0]); prtTimeStamp(ts_data[1]); print();
                j = j+1
                #break
            else :#COLLECT 200 DATA FROM SMARTMETERS
                if (b'END' in data) :
                    conn.sendall(buf+data)
                    buf=''.encode()
                    #print('Received', repr(data))
                    strdata = str(data)[2:-1] #to remove the 'b   '
                    dw = strdata.split(',')
                    #print(dw)
                    
                    #if i in range(200):
                    ii = int(dw[0]) #for capture the Meter-ID
                    ts_data[ii][0] = ii #ID-Meter
                    ts_data[ii][1] = float(dw[1]) #Timestamp()
                    ts_data[ii][2] = float(dw[2]) #Usages
                    ts_data[ii][3] = dw[3] #Status END means empty/original status
                    
                else:
                    buf= buf + data #+'-'.encode()
