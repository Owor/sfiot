"""**************************************************************************************
*   Author  : Yong-Hong                                                                 *
*   Date    : 2020/04/09                                                                *
*   Describe: this program is for IoT container and it is main thread.                  *
**************************************************************************************"""
###
# Message staus
'''
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
from socket_lib.socket_listen_for_inner import listen_inner_network
from socket_lib.script import run
from socket_lib.thread_lib import stop_thread

from IoT_to_BC_and_DNN import SendData_to_BC_DNN
#==variable=====================================================================================================
CONTAINER_NAME_IOT = "container_I_0"     # IOT container's name
CONTROL_PORT_BC = 12345                 # The port of BC container's control channel.
CONTROL_PORT_IOT = 12346              # The port of IOT container's control channel.
CONTROL_PORT_DNN = 12347              # The port of DNN container's control channel.

csv_path_iot = "container_port_IOT.csv"
#====================================================================================================================
class subthread_iot():
    def __init__(self):
        self.message = ""
        self.instruction = ""
        self.thread = []
        self.port = []
#--------------------------------------------------------------------------------------------------------------
    #def IoT_addThread_for_client(self,port):
        # To create new thread for send meter data
#--------------------------------------------------------------------------------------------------------------
    def run(self,control_port):

        print("IOT's control port started to listen !")
        while True:
            
            self.instruction, self.message = listen_control_message(control_port)
            
            print(self.instruction)

            # Update model
            if self.instruction == "00":
                #do not do anything
                print("do not do anything")

            # Finished Update model
            elif self.instruction == "01":
                #do not do anything
                print("do not do anything")

            # Update the table add record
            elif self.instruction == "10":
                container_name, new_port = self.message.split(":")
                Update_port_add(csv_path_iot, container_name, int(new_port))
                print("Updated table. ")    #check thread array

            # Update the table delete record
            elif self.instruction == "11":
                container_name, old_port = self.message.split(":")
                Update_port_delete(csv_path_iot, container_name, int(old_port))
                print("Updated table. ")    #check thread array
            # Error message
            else:
                print("The message is not expect. ")
            
#==================================================================================================================
if __name__ == "__main__":
    control_channel = subthread_iot()
     #-----create the thread for receive data from Lora------
        #coding here
    #-----create finish--------------------------------------


    #-----create the thread for iot to BC & DNN------
    IoT_to_BC_DNN_thread = th.Thread(target = SendData_to_BC_DNN, args=[0])    #The data thread which send data to BC and DNN.
    IoT_to_BC_DNN_thread.start()
    print("===============================================================")
    #-----create finish------------------------------
    control_channel.run(CONTROL_PORT_IOT)
