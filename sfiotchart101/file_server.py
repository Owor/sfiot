import socket
import os

HOST = "127.0.0.1"
PORT = 25000
savepath = "lib/model_file_folder/new_model.h5"
#==========================================================================
def fileserver():

    while True:
        buf = []        #receive buffer

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(1)

            print("Server is already listen on port: "+ str(PORT) +" ...")
            
            conn, addr = s.accept()
            print('Connected by', addr)
            
            with conn:
                while True:
                    data = conn.recv(1024)
                    #print(data)
                    print(str(len(buf)) +"================================================")
                    if "final".encode('utf-8') in data:
                        break
                    else:
                        buf.append(data)
            conn.close()
            s.close()
        #----------------------------------------------------------
        #print(buf)
        print(buf[639])

        f = open(savepath, 'wb')
        for data in buf:
            f.write(data)

        print("File stored!")
        f.close()
#=============================================================================================
#=============================================================================================
if __name__ == "__main__":
    fileserver()