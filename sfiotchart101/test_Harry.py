#!/usr/bin/env python3

import socket
import sys
import argparse
from lib.modify_container_port import get_UsablePort
from socket_lib.client_for_inner import socket_connect_once

# HOST = '172.17.0.2' # container
HOST = '127.0.0.1'
#HOST = '192.168.112.133' # host
PORT = 12345
#=====================================================================================
#=====================================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Please enter command: ')
    parser.add_argument("-c", "--command", type=str, default="NULL", help='Enter command.')
    parser.add_argument("-p", "--port", type=str, default="NULL", help='Enter command.')
    arg= parser.parse_args()
    if arg.port != "NULL":
        socket_connect_once(int(arg.port),"testdata............")
    else:
        if(arg.command == "00"):
            print("found new model!")
            socket_connect_once(PORT,"00,")
        elif(arg.command == "01"):
            socket_connect_once(PORT,"01,")

    #socket_connect_once("10,container_M_0:"+ str(get_UsablePort("container_port_BC.csv")))
    #socket_connect_once("11,container_M_0:"+ str(6002))
