import socket

def gethostIP():
   try:
       host_name = socket.gethostname()
       host_ip = socket.gethostbyname(host_name)
       print("Hostname: ", host_name)
       print("IP: ", host_ip)
       return host_ip
   except:
       print("Unable to get Hostname or IP")

print(gethostIP())
