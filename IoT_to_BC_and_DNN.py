"""**************************************************************************************
*   Author  : Yong-Hong                                                             	*
*   Date    : 2020/04/22                                                            	*
*   Describe: this program is for Iot subthread and it will send data to BC and DNN.	*
**************************************************************************************"""

from socket_lib.client_for_inner import socket_connect_END
#from socket_lib.client_for_inner_1 import socket_connect
import time
import pickle
import argparse
import time

#****************Load Data**************************************
import pandas as pd
data_path = "socket_lib/Residential-Profiles_Plus_AVG_SORT.csv"	#csv file path

dataset = pd.read_csv(data_path)
title = dataset.columns[1:].tolist()

timestep = dataset['Time'].tolist()
num_rows = len(timestep)

read_data = dataset.values[:, 1: ]  #get 1 to 201   total: 200
num_cols = len(title)

print(dataset.values.shape)
print(read_data.shape)

print(num_rows)
print(num_cols)

HOST = "127.0.0.1"
DNN_data_port = 10000
BC_data_port = 10001
#=====================================================================================================
def SendData_to_BC_DNN(flag):
	print("subthread : Iot to BC & DNN start! ...")
	row_data = []

	for row in range(0, num_rows):
		for col in range(0, num_cols):
			print(col)
			row_data.append(str(title[col])+";2019-12-05,00:00:"+ str(int(timestep[row])) +";N;"+ str(read_data[row][col]) +";GatewayID;END")
			print(row_data)

			#socket_connect_END(BC_data_port, row_data, 1)		#send data to BC
			socket_connect_END(DNN_data_port, row_data, 1)		#send data to DNN

			row_data.clear()	#clear buffer
			time.sleep(2)
		print("===========================================")
		
		if(row >=40000):
			break

""" data format : H-XX;2019-12-05,00:00:00;N;XX.X;GatewayID;END """

#====================================================================================================
#====================================================================================================
if __name__ == "__main__":
	row_data = []
	for row in range(0, num_rows):
		#print(row)
		for col in range(0, num_cols):
			temp = str(title[col])+";2019-12-05,00:00:"+ str(int(timestep[row])) +";N;"+ str(read_data[row][col]) +";GatewayID;END"
			row_data.append(temp)

	print("data prepare finished")
	socket_connect_END(DNN_data_port, row_data, 40000)		#send data to DNN
	#SendData_to_BC_DNN(1)
	"""
	parser = argparse.ArgumentParser(description='Please enter port: ')
	parser.add_argument("-p", "--port", type=str, default="NULL", help='Enter port number')

	args = parser.parse_args()

	if args.port !="NULL":
		senddata200(int(args.port))
	"""

