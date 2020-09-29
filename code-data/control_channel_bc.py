"""**********************************************************************************
*   Author  : Yong-Hong                                                             *
*   Date    : 2020/04/09                                                            *
*   Describe: this program is for Block-Chain container and it is main thread .     *
**********************************************************************************"""
###
# Message staus
'''
00 : create new thread
01 : stop old thread
10 : Update the table (add)
11 : update the table (delete)
'''
###

# Import module
import threading as th
from setting import *


# ./lib module
from lib.modify_container_port import Update_port_add
from lib.modify_container_port import Update_port_delete
from lib.modify_container_port import get_UsablePort
from socket_lib.socket_listen_for_inner import listen_control_message
from socket_lib.client_for_inner import socket_connect_once
from socket_lib.script import run
from socket_lib.thread_lib import stop_thread
from socket_lib.thread_lib import stop_thread_safe
from BC_receiver import BC_receiver_run

#==variable=====================================================================================================
CONTAINER_NAME_BC = "container_B_0"     # BC container's name
CONTROL_PORT_BC = 12345                 # The port of BC container's control channel.
CONTROL_PORT_IOT = 12346              # The port of IOT container's control channel.
CONTROL_PORT_DNN = 12347              # The port of DNN container's control channel.

csv_path_bc = "container_port_BC.csv"
#====================================================================================================================
class subthread_bc():
    def __init__(self):
        self.message = ""
        self.instruction = ""
        self.thread = []
        self.port = []
        self.socket_temp = []
#--------------------------------------------------------------------------------------------------------------
    def bc_addThread_for_listen(self, port):
        self.thread.append(th.Thread(target = BC_receiver_run, args=(1, port)))    #start a new thread
    
        self.thread[-1].start()

        Update_port_add(csv_path_bc, CONTAINER_NAME_BC,port)     # start a thread for BC received data, need update port table.
        
        #-----send "10" to each container for update those port table.-----
        socket_connect_once(CONTROL_PORT_IOT,"10,"+ CONTAINER_NAME_BC +":"+ str(port))        # send to iot container.

        socket_connect_once(CONTROL_PORT_DNN,"10,"+ CONTAINER_NAME_BC +":"+ str(port))           # send to DNN container.
#--------------------------------------------------------------------------------------------------------------
#******************************************************************************************************
#* Function: run                                                                                      *
#* Describe: This function is for main thread of BC container.                                        *
#* @para| self |: python class need.                                                                  *
#* @para| control_port |: BC container's control(main) thread listen port.                            *
#******************************************************************************************************
    def run(self, control_port):
        print("BC's controll port started to listen !")

        while True:
            self.instruction, self.message = listen_control_message(control_port)

            print(self.instruction)

            # Update model
            if self.instruction == "00":
                self.port.append(int(get_UsablePort(csv_path_bc)))      # get usableport and append to port[].
                print(self.port)                                                    # check the port list.
                self.bc_addThread_for_listen(self.port[-1])                         # start a thread and listen on newest port for data.

                print(self.thread)      #check thread list
            #---------------------------------------------------------------------------   
            # Finished Update model
            elif self.instruction == "01":
                #stop_thread(self.thread[0])
                stop_thread_safe(self.port[0])
                self.thread.pop(0)
                print(self.thread)
                
                Update_port_delete(csv_path_bc, CONTAINER_NAME_BC,self.port[0])
                print("Updated table. ")    #check thread array

                #-----send "11" to each container for update those port table delete.---------
                socket_connect_once(CONTROL_PORT_IOT,"11,"+ CONTAINER_NAME_BC +":"+ str(self.port[0]))    # send to iot container.

                socket_connect_once(CONTROL_PORT_DNN,"11,"+ CONTAINER_NAME_BC +":"+ str(self.port[0]))    # send to dnn container.
                #-----------------------------------------------------------------------------

                self.port.pop(0)             #delete oldest port
                print(self.port)
            #---------------------------------------------------------------------------
            # Update the table add record
            elif self.instruction == "10":
                container_name, new_port = self.message.split(":")
                Update_port_add(csv_path_bc, container_name, int(new_port))
                print("Updated table. ")    #check thread array
            #---------------------------------------------------------------------------
            # Update the table delete record
            elif self.instruction == "11":
                container_name, old_port = self.message.split(":")
                Update_port_delete(csv_path_bc, container_name, int(old_port))

                print("Updated table. ")    #check thread array
                
            # Error message
            else:
                print("The message is not expect. ")
            
#==================================================================================================================
#==================================================================================================================
if __name__ == "__main__":
    control_channel = subthread_bc()
    BC_receive_from_iot_thread = th.Thread(target = BC_receiver_run, args=(0, 10001))    #first data thread which Receiving data from iot always listen on 10001 port.
    BC_receive_from_iot_thread.start()
    print("The port witch receiving data from iot is listening!, port: 10001")
    print("===============================================================")
    control_channel.thread.append(th.Thread(target = BC_receiver_run, args=(0, 6001)))     #first data thread which Receiving data from DNN always listen on 6001 port. 
    control_channel.port.append(6001)       #storing the thread which receiving from DNN to port queue.
    
    control_channel.thread[-1].start()      #data thread which from DNN start.
    print(control_channel.thread)
    
    control_channel.run(CONTROL_PORT_BC)    #control thread start.
