import subprocess
import csv
import sys
import os
import argparse


def run_main_container(mangement_container_name,container_name,docker_version_name = "mytomcat2"):
    try:
        result = subprocess.check_call("sudo docker run  --name "+container_name+" --net=container:"+mangement_container_name+" -it "+docker_version_name, shell=True)
        print(result)
    except subprocess.CalledProcessError as err:
        print("Command Error")
#========================================================================================================
def delete_all_container():
    try:
        subprocess.check_call("sudo docker stop $(sudo docker ps -a -q)", shell=True)
        subprocess.check_call("sudo docker rm $(sudo docker ps -a -q)", shell=True)

    except subprocess.CalledProcessError as err:
        print("Command Error")
#========================================================================================================
"""***************************************************************************************************
*   Function : delete_container                                                                      *
*   Describe : Delete the container (only one container)                                             *
*   @Para (String)    | container_name | : The container's name which want to delete container.      *
***************************************************************************************************"""
def delete_container(container_name):
    try:
        subprocess.check_call("sudo docker stop "+container_name, shell=True)
        subprocess.check_call("sudo docker rm "+container_name, shell=True)

    except subprocess.CalledProcessError as err:
        print("Command Error")
#========================================================================================================
def show_all_container():
    try:
        subprocess.check_call("sudo docker ps -a", shell=True)

    except subprocess.CalledProcessError as err:
        print("Command Error")
#========================================================================================================
# def stop_container(container_name):
#     try:
#         subprocess.check_call("sudo docker stop "+container_name, shell=True)

#     except subprocess.CalledProcessError as err:
#         print("Command Error")

#========================================================================================================
def build_container(image_name):
    try:
        subprocess.check_call("sudo docker build -t "+image_name +" . --no-cache", shell=True)
    except subprocess.CalledProcessError as err:
        print("Command Error")
#========================================================================================================
def run_container(mangement_container_name, image_name):
    
    try:
        subprocess.check_call("sudo docker run --name "+mangement_container_name+" -it "+image_name, shell=True)
    except subprocess.CalledProcessError as err:
        print("Command Error")
    return mangement_container_name
#========================================================================================================
def run_container_background(mangement_container_name, image_name):
    
    try:
        subprocess.check_call("sudo docker run --name "+mangement_container_name+" -d "+image_name, shell=True)
    except subprocess.CalledProcessError as err:
        print("Command Error")
    return mangement_container_name
#========================================================================================================
# def copy_file_to_container(filename):
#     try:
#         subprocess.check_call("sudo docker build -t "+image_name +" . --no-cache", shell=True)
#     except subprocess.CalledProcessError as err:
#         print("Command Error")

