"""**************************************************************************************
*   Author  : Yong-Hong                                                                 *
*   Date    : 2020/04/09                                                                *
*   Describe: this program is for DNN container and it is main thread.                  *
**************************************************************************************"""
###
# Message staus
'''
00 : create new thread
01 : stop old thread
10 : Update the table (add)
11 : update the table (delete)
'''
###

#===========import====================================================================================================
import time
import os
import threading as th
from setting import *



from lib.modify_container_port import Update_port_add
from lib.modify_container_port import Update_port_delete
from lib.modify_container_port import get_UsablePort
from socket_lib.socket_listen_for_inner import listen_control_message
from socket_lib.client_for_inner import socket_connect_once
from socket_lib.script import run
from socket_lib.thread_lib import stop_thread
from socket_lib.thread_lib import stop_thread_safe
from BC_receiver import BC_receiver_run

from lib.DNN_timer import check_model_file
from lib.DNN_timer import Is_new_model_file_exist
from lib.DNN_timer import received_filepath
from lib.DNN_timer import removefile_and_setflag

from test_thread import test_thread
from test_thread import test_receive

from file_server import fileserver

#========variable=====================================================================================================
CONTAINER_NAME_DNN = "container_D_0"     # DNN container's name
CONTROL_PORT_BC = 12345                 # The port of BC container's control channel.
CONTROL_PORT_IOT = 12346              # The port of IOT container's control channel.
CONTROL_PORT_DNN = 12347              # The port of DNN container's control channel.

csv_path_dnn = "container_port_DNN.csv"
old_model_file_path = "old_model_path"
new_model_filepath = "lib/model_file_folder/new/new_model.h5"   # 要檢查的檔案路徑
update_flag = False
#====================================================================================================================
class subthread_dnn():
    def __init__(self):
        self.message = ""
        self.instruction = ""
        self.thread = []
        self.port = []
        self.socket_temp = []
#--------------------------------------------------------------------------------------------------------------
    def dnn_createThread_and_load_model(self, port, model_file_path):
        #self.thread.append(th.Thread(target = """here need put DNN client function""", args=(0, port, model_file_path)))    #start a new thread

        #********For simulate update model operation****************************
        self.thread.append(th.Thread(target = test_thread, args=(1, port, model_file_path)))     #first data thread always listen on 6000 port. 
        print("listen on "+ str(port) +"port")
        #*********************************************************************** 
        self.thread[-1].start()

        Update_port_add(csv_path_dnn, CONTAINER_NAME_DNN, port)     # start a thread for BC received data, need update port table.
        
        #-----send "10" to each container for update those port table.-----
        socket_connect_once(CONTROL_PORT_IOT,"10,"+ CONTAINER_NAME_DNN +":"+ str(port))        # send to iot container.

        socket_connect_once(CONTROL_PORT_BC,"10,"+ CONTAINER_NAME_DNN +":"+ str(port))            # send to bc container.
        #------------------------------------------------------------------
        time.sleep(2)
        #-----send "00" to bc container for update model process.------
        socket_connect_once(CONTROL_PORT_BC,"00,")        # send to bc container.
#--------------------------------------------------------------------------------------------------------------

#******************************************************************************************************
# Function: run                                                                                       *
# Describe: This function is for main thread of DNN container                                         *
# @para| self |: python class need                                                                    *
# @para| control_port |: DNN container's control(main) thread listen port                             *
#******************************************************************************************************
    def run(self,control_port):
        print("DNN's controll port started to listen !")
        while True: 
            print("Main thread still running...")     
            time.sleep(3)  
            update_flag = Is_new_model_file_exist()
            if update_flag:
                os.system("mv "+ received_filepath +" "+ new_model_filepath)
                print("======================== move file finished! ... ============================")
                self.port.append(int(get_UsablePort(csv_path_dnn)))      # get usableport and append to port[].
                print(self.port)                                                        # check the port list.
                self.dnn_createThread_and_load_model(self.port[-1], new_model_filepath)                # start a thread and listen on newest port for data.

                print(self.thread)      #check thread list
    #---------------change to update mode-----------------------------------------
                while Is_new_model_file_exist():
                    self.instruction, self.message = listen_control_message(control_port)   #receive message.
                    
                    print(self.instruction)

                    # Update model
                    if self.instruction == "00":
                        break
                    #---------------------------------------------------------------------------   
                    # Finished Update model
                    elif self.instruction == "01":
                        stop_thread_safe(self.port[0])
                        self.thread.pop(0)
                        print(self.thread)
                        
                        Update_port_delete(csv_path_dnn, CONTAINER_NAME_DNN,self.port[0])
                        print("Updated table. ")    #check thread array

                        #-----send "11" to each container for update those port table delete.---------
                        socket_connect_once(CONTROL_PORT_IOT,"11,"+ CONTAINER_NAME_DNN +":"+ str(self.port[0]))    # send to iot container.

                        socket_connect_once(CONTROL_PORT_BC,"11,"+ CONTAINER_NAME_DNN +":"+ str(self.port[0]))    # send to bc container.
                        #-----------------------------------------------------------------------------

                        self.port.pop(0)             #delete oldest port
                        print(self.port)

                        time.sleep(3)
                        
                        socket_connect_once(CONTROL_PORT_BC,"01,")          # send "01," to BC container to continue update process.
                    #---------------------------------------------------------------------------------
                    # Update the table add record
                    elif self.instruction == "10":
                        container_name, new_port = self.message.split(":")
                        Update_port_add(csv_path_dnn, container_name,int(new_port))
                        print("Updated table. ")    #check thread array
                    #---------------------------------------------------------------------------
                    # Update the table delete record
                    elif self.instruction == "11":
                        container_name, old_port = self.message.split(":")
                        Update_port_delete(csv_path_dnn, container_name,int(old_port))
                        print("Updated table. ")    #check thread array

                        removefile_and_setflag()      #delete new model file and set flage to false.
                    # Error message
                    else:
                        print("The message is not expect. ")
            
#==================================================================================================================
#==================================================================================================================
if __name__ == "__main__":
    #********data thread which Receiving data from iot***********************
    control_channel = subthread_dnn() #DNN main thread test_thread
    DNN_receive_from_iot_thread = th.Thread(target =test_receive, args=(0, 10000))    #first data thread which Receiving data from iot always listen on 10000 port.
    DNN_receive_from_iot_thread.start()
    print("The port which receiving data from iot is listening!, port: 10000")
    #***********************************************************************

    #********For simulate file server to receive file***********************
    fileserver_thread = th.Thread(target = fileserver, args=())     #reeive file thread listen on 25000 port.  
    fileserver_thread.start()        #Data thread start.
    print("The port which receiving file from server is listening!, port: 25000")
    #***********************************************************************

    # control_channel.thread.append(th.Thread(target = """here need put DNN server(model) function""", args=(0, 6000, old_model_path)))     #first data thread always listen on 6000 port.  
    # control_channel.port.append(6000)           #Storing the thread which receiving data from DNN to port queue.
    # control_channel.thread[-1].start()        #Data thread start.
    # print(control_channel.thread)


    #********For simulate update model operation****************************
    control_channel.thread.append(th.Thread(target = test_thread, args=(0, 6000, old_model_file_path)))     #first data thread listen on 6000 port.  
    control_channel.port.append(6000)           #Storing the thread which receiving data from DNN to port queue.
    control_channel.thread[-1].start()        #Data thread start.
    print(control_channel.thread)
    #***********************************************************************
    

    check_model_file()              #Start the timer which checking new model file.
    control_channel.run(CONTROL_PORT_DNN)    #Control(main) thread start.
