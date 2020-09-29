"""**********************************************************************************************
*   Author  : Yong-Hong                                                             	        *
*   Date    : 2020/06/03                                                            	        *
*   Describe: This is a libaray for dnn main thread to check new model file is exist or not.    *
**********************************************************************************************"""
#*********import*************************************************************************************
from threading import Timer
import time 
import os

#*********variable declare***************************************************************************
FILE_FLAG = False

received_filepath = "lib/model_file_folder/new_model.h5"   # 要檢查的檔案路徑


#*********function declare***************************************************************************
"""******************************************************************************************************
* Function: check_model_file                                                                            *
* Describe: This function is for main thread to detect the new model file is exist or not.              *
******************************************************************************************************"""
def check_model_file(): 
    global FILE_FLAG

    if not FILE_FLAG:   #This is to solve synchronic problem.
        print("checking~~~~!!!!")      
        
        # 檢查檔案是否存在
        if os.path.exists(received_filepath):
            print("file exist !")
            FILE_FLAG = True
        else:
            print("file is not exist !")
            FILE_FLAG = False
    #****************************************************
    # repeat the timer, because it only execute one time.
    file_check_timer = Timer(5, check_model_file)
    file_check_timer.start()
#===================================================================================================
"""******************************************************************************************************
* Function: Isexist                                                                                     *
* Describe: This function will return the flag of file exist.                                           *
* return| type:boolean |:   False: file does exist | True: file does exist                              *
******************************************************************************************************"""
def Is_new_model_file_exist(): 
    global FILE_FLAG
    
    return FILE_FLAG
#===================================================================================================
"""******************************************************************************************************
* Function: setflag                                                                                     *
* Describe: This function will set flag to you want.                                                    *
* @para| bool:boolean |:   False: set falg to False | True: set falg to true                            *
******************************************************************************************************"""
def removefile_and_setflag(): 
    global FILE_FLAG

    try:
        os.remove(received_filepath)
    except OSError as e:
        print(e)
    else:
        print("delete finished!")
        FILE_FLAG = False
#====================================================================================================
#====================================================================================================
if __name__ == "__main__":
    check_model_file()
    while(True):
        #do nothing
        if FILE_FLAG:
            print("creating sub thread and load new model file")
            try:
                os.remove(filepath)
            except OSError as e:
                print(e)
            else:
                print("delete finished!")
                FILE_FLAG = False

        time.sleep(10)