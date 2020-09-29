import csv
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from setting import *

def check_no_same_port(new_port = None):

    with open(CONTAINER_PORT, newline='') as csvfile:
        # Read CSV to dictionary
        rows = csv.DictReader(csvfile)

        temp = None
        print("Check....")
        for row in rows:
            if row['port'] != str(new_port):
                temp = row['port']
                
        if temp is None:
            return None
        return int(temp) + 1


def get_free_port():
    new_port = check_no_same_port()

    if new_port is None:
        return DEFINE_PORT

    elif new_port is not None:
        return int(new_port) + 1
    else:
        print("Check_no_same_port Error .")


def write_new_data(container_name,port):
    f = open(CONTAINER_PORT, 'a', newline='')
    writer = f.write(container_name+","+port+'\n')
    
if __name__ == "__main__":
    port = get_free_port()
    print(port)
