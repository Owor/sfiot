
FILE_PATH = "container_port.csv"
MIN_PROT = 6000
MAX_PORT = 6009 #port range 6000 ~ 6009
#=================================================================================================================
"""***************************************************************************************
* Update_port_delete: add a record to port table.                                        *
* @para| container_name |: The container_name.                                           *
* @para| new_port |: The port which your want to add.                                    *
***************************************************************************************"""
def Update_port_add(filepath,container_name, new_port):   #for "01" instruction add record
    container_port_file = open(filepath, 'r+')
    w_str = ""
    flag = 0

    for line in container_port_file.readlines():
        if "name" in line:  #ignore first row
            w_str += line 
            continue
        else:
            #------------for sort-------------
            temp_port = int(line.split(",")[1])
            if new_port < temp_port: #  <
                if flag == 0:
                    w_str += container_name +","+ str(new_port)+"\n"        
                    flag = 1
            w_str += line
            #---------------------------------
    container_port_file.close()
    if flag == 0:   #for last
        w_str += container_name +","+ str(new_port)+"\n"


    recover_file = open(filepath, 'w')    #recover port file
    recover_file.write(w_str)
    recover_file.close()
#--------------------------------------------------------------------------------------------------------------
"""***************************************************************************************
* Update_port_delete: delete a record from port table.                                   *
* @para| container_name |: The container_name.                                           *
* @para| old_port |: The port which your want to delete.                                 *
***************************************************************************************"""
def Update_port_delete(filepath,container_name, old_port):   #for "11" instruction delete record
    container_port_file = open(filepath, 'r+')
    w_str = ""
    flag = 0

    for line in container_port_file.readlines():
        if "name" in line:  #ignore first row
            w_str += line 
            continue
        else:
            #------------for sort-------------
            temp_port = int(line.split(",")[1])
            if old_port == temp_port: #  ==
                if flag == 0:      
                    flag = 1
                    continue
            w_str += line
            #---------------------------------
    container_port_file.close()

    recover_file = open(filepath, 'w')    #recover port file
    recover_file.write(w_str)
    recover_file.close()
#--------------------------------------------------------------------------------------------------------------
"""***************************************************************************************
* get_UsablePort: find port table and get a usable port.                                 *
* return| type:int |: 0: cannot found | >0: found a usable port                          * 
***************************************************************************************"""
def get_UsablePort(filepath):
    container_port_file = open(filepath, 'r+')
    find_port = MIN_PROT
    for line in container_port_file.readlines():
        if "name" in line:  #  ignore first row
            continue
        else:
            temp_port = int(line.split(",")[1])
            if temp_port == find_port:
                find_port += 1
            else:   #  found
                break
    
    if find_port > MAX_PORT:
        return 0
    else:
        return find_port

#======================================================================================
if __name__ == "__main__":
    #Update_port_add(FILE_PATH,"container_M_0",6003)
    #Update_port_delete(FILE_PATH,"container_M_0",6002)
    print(str(get_UsablePort(FILE_PATH)))