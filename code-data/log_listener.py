import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

import sqlite3
from sqlite3 import Error

sm_list = []
class log_listener():
    def __init__(self):
        self.conn = self.create_connection("./db/smartgw_log.db")

    def create_connection(self,db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        
        return None

    # def get_recv_data(gatewayID, numfailedSM, timestamp, sm_list):
    #     conn = create_connection("db\smartgw_log.db")
    #     with conn:
    #         recvlog = (gatewayID,numfailedSM,timestamp)
    #         lrlogid = store_recv_log(conn,recvlog)
    #         for sm in sm_list:
    #             smFailedlog = (sm,timestamp,lrlogid)
    #             resultId = store_smFailed_log(conn,smFailedlog)
    #             print(resultId)

    def get_data(self, gatewayID, data, timestamp, sm_list, tag):
        with self.conn:
            dnnlog = (gatewayID,data,timestamp)
            dnnlogid = self.store_dnn_log(self.conn,dnnlog)
            for sm in sm_list:
                if tag == "anomaly":
                    anlomalylog = (sm,dnnlogid)
                    resultId = self.store_Anomaly_log(self.conn,anlomalylog)
                    print(resultId)
                elif tag == "smfailed":
                    smFailedlog = (sm,lrlogid)
                    resultId = self.store_smFailed_log(self.conn,smFailedlog)
                    print(resultId)
                else:
                    print("The tag is null or not exist .")

    # def store_recv_log(self, conn, recvlog):
    #     """
    #     Create a new LoRa Receiver Log into the LoRa_Receiver_Log table
    #     :param conn:
    #     :param recvlog:
    #     :return: LRLogId
    #     """
    #     sql = ''' INSERT INTO LoRa_Receiver_Log(GatewayID,NumFailedSM,timestamp)
    #             VALUES(?,?,?) '''
    #     cur = conn.cursor()
    #     cur.execute(sql, recvlog)
    #     return cur.lastrowid

    def store_smFailed_log(self, conn, smFailedlog):
        """
        Added Failed SM ID into the Failed_SM_Log table
        :param conn:
        :param smFailedlog:
        :return: FSMLogId
        """
        sql = ''' INSERT INTO Failed_SM_Log(SMId,LRLogId)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, smFailedlog)
        return cur.lastrowid

    def store_dnn_log(self, conn, dnnlog):
        """
        Create a new DNN Log into the DNN_Log table
        :param conn:
        :param dnnlog:
        :return: DnnLogId
        """
        sql = ''' INSERT INTO DNN_Log(GatewayID,Data,timestamp)
                VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, dnnlog)
        return cur.lastrowid

    def store_Anomaly_log(self, conn, anlomalylog):
        """
        Added SM ID with anomaly data into the Anomaly_Log table
        :param conn:
        :param anlomalylog:
        :return: AnlomalyId
        """
        #maybe next can classify what kind of anomaly (hacked, thief, or etc)

        sql = ''' INSERT INTO Anomaly_Log(SMId,DnnLogId)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, anlomalylog)
        return cur.lastrowid
