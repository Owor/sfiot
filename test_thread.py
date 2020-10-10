import time
from socket_lib.socket_listen_for_inner import listen_inner_network_END
from DNN_to_BC import senddata200

def test_thread(flag, port, model_file_path):
	
	if flag is 0:
		print("old_model was load!, port :"+ str(port) +"| loading from "+ model_file_path)
	elif flag is 1:
		print("new model was load!, port :"+ str(port) +"| loading from "+ model_file_path)
	
		time.sleep(15)
		print("new model does finished the data collection")
		senddata200(6003)

	while True:
		total_data = listen_inner_network_END(port)
		if "ESC" in total_data[0]:
			print("Stoped!")
			break			#quit thread in a safe method.
		else:
			print(total_data)
#===================================================================================================
def test_receive(flag, port):
	while True:
		total_data = listen_inner_network_END(port)
		if "ESC" in total_data[0]:
			print("Stoped!")
			break			#quit thread in a safe method.
		else:
			print(total_data)
