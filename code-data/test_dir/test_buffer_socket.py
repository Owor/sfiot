
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../socket_lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from socket_listen_for_inner import *
from design_buff import *


if __name__ == "__main__":
    a = design_buff()
    while True:
        value = listen_inner_network(6000)
        dict_data = {"id":value[0][-1:],"time":value[1],"power":value[2]}
        if value != None:
            a.run_buff(dict_data)
            result_array = a.show_buff()
            print(result_array)
            print("\n ++++++++++++++++++++\n")

