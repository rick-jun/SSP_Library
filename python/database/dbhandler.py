import sys
import sqlite3
import json

from ssp.sqlitehandler import SQLiteHandler
from ssp.mqclient import MQClient
from ssp.mariadbhandler import MariaDBHandler

class DBHandler:
    '''
    Used to handle all DB handling jobs without locking DB.
    '''
    # -----------------------------------------------------------------------------------------------
    def __init__(self, configs):
        try:
            self.configs = configs
            
            # self.sqlitedb = sqlite3.connect(self.configs["Database"]["sqlite_file_path"])
            self.mq_client = MQClient()
            self.mq_client.connect(self.configs["MQ"]["BrokerIP"], self.configs["MQ"]["BrokerPort"])       
            sub_topic_info = (self.configs["MQ"]["ToDBTopic"], 0)
            self.mq_client.subscribe(sub_topic_info)
            self.mq_client.on_message = self.on_to_db_message
            
            self.db = MariaDBHandler(configs)

            print(f'DBHandler cretaed.')
        except Exception as e:
            print(f"Error at [{self.__class__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")
    
    # -----------------------------------------------------------------------------------------------
    def loop_start(self):
        self.mq_client.loop_start()
        
    # -----------------------------------------------------------------------------------------------
    def on_to_db_message(self, client, userdata, msg):

        '''
        알람 시작 시 { 'start': 'YYYYMMDD_HHmmss', 'end': '-', 'confidence': 0.312, 'filename': 'YYYYMMDD_HHmmss.jpg' }
        알람 종료 시 { 'start': 'YYYYMMDD_HHmmss', 'end': 'YYYYMMDD_HHmmss', 'confidence': 0.423, 'filename': 'YYYYMMDD_HHmmss.jpg'}
        '''
        data = json.loads(msg.payload.decode())

        try:
            tablename = data["table"]
            data.pop('table', None)
            self.db.insert(tablename=tablename, column_values=data)
            
        except Exception as e:
            print(f"Error at [{self.__class__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")

    # -----------------------------------------------------------------------------------------------
    def __del__(self):
        pass
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
# ===================================================================================================
if __name__ == '__main__':
    pass