"""**************************************************************************************
*   Arthor  : Yong-Hong                                                             	*
*   Date    : 2020/05/20                                                            	*
*   Describe: this program is a script for automatically build container	            *
**************************************************************************************"""
import subprocess
import csv
import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

from docker_tool import *
#===variable declare===============================================================================
all_category = ['IOT','DNN','BC']

image_name = ["iot_container_image", "dnn_container_image", "bc_container_image"]
CONTAINER_NAME_IOT = "container_I_0"     # IOT container's name
#==================================================================================================
#==================================================================================================
if __name__ == "__main__":
    #build_container(image_name[0])      # build iot_container's image
    #print("~~~~~~~~~~~~~~build " + image_name[0] + "finished!~~~~~~~~~~~~")
    #run_container(CONTAINER_NAME_IOT,image_name[0])     # run iot_container by load iot_container image
    #print("~~~~~~~~~~~~~~run " + CONTAINER_NAME_IOT + "finished!~~~~~~~~~~~~")

    run_container_background(CONTAINER_NAME_IOT,image_name[0])
    print("~~~~~~~~~~~~~~run in background " + CONTAINER_NAME_IOT + "finished!~~~~~~~~~~~~")

    #**********************BC part**********************
    # Build BC container image
    # Run BC image (Container)
    #***************************************************

    #***********************DNN part********************
    # Build DNN container image
    # Run DNN image (Container)
    #***************************************************