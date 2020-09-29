import subprocess
import csv
import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

from modify_dockerfile import modify_dockerfile_port
from modify_dockerfile import modify_socket_port
from create_container_name import get_new_container_name
from docker_tool import *

all_category = ['IOT','DNN','BC']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Please enter images name: ')
    parser.add_argument("-n", "--name", type=str, default="NULL", help='Enter images name')
    parser.add_argument("-c", "--category", type=str, default="NULL", help='Chooses category')
    parser.add_argument("-m", "--memory", type=str, default="NULL", help='Craeate memory size')
    parser.add_argument("-d", "--delete", type=str, default="NULL", help='Delete all container')
    parser.add_argument("-b", "--build", type=str, default="NULL", help='Build images T/F')
    args = parser.parse_args()

    if args.delete != "NULL":
        print("------------Start delete images------------------")
        if args.delete == "all":
            print("------------delete all images------------------")
            delete_all_container()
        else :
            print("------------delete "+args.delete+"-------------------")
            delete_container(args.delete)
        show_all_container()

    category = ""
    mangement_container_name = ""
    container_name = ""



    if args.category != "NULL":
        args.category = args.category.upper()
        category = args.category

        mangement_container_name = "container_M_0"
        if category == "DNN" or category == "BC" :
            print("Create container category "+args.category)
            # Get the container's name
            container_name = get_new_container_name(category)
            # Modify dockerfile from /example/DNN or /example/BC about adding the port
            modify_dockerfile_port(container_name, category)
            # Modify file from /socket_lib/socker_for_inner.py about adding the port
            modify_socket_port(container_name)

        elif category == "IOT":
            print("Create container category "+args.category)

            # Manage container' name is used to copying network in docker platform or creating manage container

            # Get the container's name
            container_name = get_new_container_name(category)
            # Modify dockerfile from /example/IOT about adding the port
            modify_dockerfile_port(container_name, category)
            # Modify file from /socket_lib/socker_for_inner.py about adding the port
            modify_socket_port(container_name)
            
        else:
            print("Don't suppert the caregory :"+category)

        try:
            # The process is about creating manage container
            if category == "IOT" and args.name != "NULL" and args.build != "NULL":
                print("Build dockerfile's named "+mangement_container_name)
                # Building Dockerfile, let the dockerfile transferring to image is named [args.name]
                build_container(args.name)
                print("Run mangement container's named " + container_name)
                # Run the image, let the image transferring to container is named "container_M_0"
                mangement_container_name = run_container(mangement_container_name, args.name)
            
            # The process is about creating IoT container by original Iot image
            elif category == "IOT" and args.name != "NULL" and  args.build == "NULL":
                # Run the image, let the image transferring to container is named [container_name]
                run_main_container(mangement_container_name, container_name, args.name)
            
            # The process is about creating BC or DNN  container
            elif category != "IOT" and args.name != "NULL" and  args.build == "NULL":
                # Building Dockerfile from /example/DNN or /example/BC, let the dockerfile transferring to image is named [args.name]
                build_container(args.name)
                # Run the image, let the image transferring to container is named [container_name]
                run_main_container(mangement_container_name, container_name, args.name)

            else :
                print("Category is : " + category)
                print("Conainer name is : " + args.name)


        except:
            print("Creating container is failed. ")
