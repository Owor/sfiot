#!/usr/bin/env python python3
import csv
CONTAINER_WORD_LENGTH = 12


def get_new_container_name(category):
    with open('./container_port.csv', newline='') as csvfile:
        # Read CSV to dictionary
        rows = csv.DictReader(csvfile)
        temp = []
        for row in rows:
            # print(row)
            temp.append(row['container_name'])
        data_length = len(temp)

        # print(data_length)
        # print(temp[data_length-1][CONTAINER_WORD_LENGTH:])
        # print(category)
        #print(int(temp[data_length-1][CONTAINER_WORD_LENGTH:])+1)

        container_name = "container_"+category[:1]+"_"+str(int(temp[data_length-1][CONTAINER_WORD_LENGTH:])+1)
        #print(container_name)
        return container_name
