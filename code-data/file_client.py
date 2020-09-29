import socket
import os
import time

#HOST = "140.123.105.200"
HOST = "127.0.0.1"
PORT = 25000
filename = "./test.h5"
#============================================================
def readfile(filename):
    buffer = [] 

    f = open(filename, "rb")
    try:
        while True:
                Bytes = f.read(1024)
                #print(Bytes)
                if Bytes == b'':
                    break # end of file
                
                buffer.append(Bytes)
                time.sleep(0.1)

    finally:
        f.close()

    return buffer
#============================================================
def socket_connect_END(host,port,data,times):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #create socket use ipv4 and TCP/IP protocol.
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)    #set reuseable time to 0s.
        s.connect((host,port))      #start to connect and wait for client connect.

    
        for i in range(0,times):
            s.sendall(data[i])
            print("send : " + str(data[i]))
            print(str(i)+"=================================================")
            time.sleep(0.01)    #important 0.005 sec to avoid dataloss
        time.sleep(1)
        s.sendall("final".encode())
        s.close()
#======================================================================================
#======================================================================================
if __name__ == "__main__":
    print("file_client  start !...")
    myfile = readfile(filename)
    print(str(len(myfile)))
    socket_connect_END(HOST, PORT, myfile, len(myfile))
