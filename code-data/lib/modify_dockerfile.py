from search_container_port import check_no_same_port
from search_container_port import write_new_data
from search_container_port import get_free_port

def modify_dockerfile_port(container_name, category):

    fopen = open("./example/"+category+"/Dockerfile", 'r+')
    w_str = ""
    
    port = str(get_free_port())
    write_new_data(container_name, port)

    # print(port)
    for line in fopen.readlines():
        if "port" in line:
            print("Before modify"+line)
            print("After modify"+line.replace("port", port))
            line = line.replace("port", port)
        w_str += line

    wopen = open("Dockerfile", 'w')
    wopen.write(w_str)
    fopen.close()
    wopen.close()
    return True

def modify_socket_port(container_name):

    fopen = open("./socket_lib/socket_listen_for_inner.py", 'r+')
    w_str = ""
    
    port = str(check_no_same_port())
    write_new_data(container_name, port)

    # print(port)
    for line in fopen.readlines():
        if "port" in line:
            print("Before modify"+line)
            line = line.replace("Enter post", port)
            print("After modify"+line)

        w_str += line

    wopen = open("./socket_lib/socket_listen_for_inner.py", 'w')
    wopen.write(w_str)
    fopen.close()
    wopen.close()
    return True
