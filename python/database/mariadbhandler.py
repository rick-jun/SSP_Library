import mariadb
import sys
import os

from ssp.confighandler import parse_json_config

class MariaDBHandler:

    @property
    def IsConnected(self):
        return self.isConnected
    
    #---------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, configs):
        self.configs = configs
        self.conn = None
        self.cur = None
        self.auto_reconnect = True
        self.isConnected = False

        self.connect()
    
    #---------------------------------------------------------------------------------------------------------------------------------
    def connect(self):
        if self.cur is None:
            if self.conn is None:
                # Connect to MariaDB Platform
                try:
                    self.conn = mariadb.connect(
                        user=self.configs["Database"]['username'],
                        password=self.configs["Database"]['password'],
                        host=self.configs["Database"]['host'],
                        port=self.configs["Database"]['port'],
                        database=self.configs["Database"]['db_name']
                    )
                    self.conn.auto_reconnect = self.auto_reconnect
                    self.isConnected = True
                except mariadb.Error as e:
                    print(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")
                    self.isConnected = False
                    return None
            
            # Get Cursor
            self.cur = self.conn.cursor()

    #---------------------------------------------------------------------------------------------------------------------------------
    # Create Connection Pool
    def create_connection_pool():
        """Creates and returns a Connection Pool"""

        # Create Connection Pool
        pool = mariadb.ConnectionPool(
            host="localhost",
            port=3306,
            user="root",
            password="",
            pool_name="web-app",
            pool_size=20,
            pool_validation_interval=250)

        # Return Connection Pool
        return pool
    
    #---------------------------------------------------------------------------------------------------------------------------------
    def insert(self, tablename, column_values, keycolumn_value=None):
        '''
        
        Parameters:
            tablename: table to insert
            column_values: Dictionary of {column name: value}
            keycolumn_value: key column name. 
        '''

        try:
            if self.cur is None:
                self.connect()
            
            query = f'INSERT INTO {tablename} ({", ".join(column_values.keys())}) VALUES ({", ".join(["?"] * len(column_values))})' 

            self.cur.execute(query, list(column_values.values()))
            self.conn.commit()

        except Exception as e:
            print(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")
            return None      
    #---------------------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        self.isConnected = False
        if self.conn is None:
            self.conn.close()

#=================================================================================================================================
if __name__ == "__main__":

    try:
        config_file = 'D:/Projects/MudQualityTracking/configs.json'

        if os.path.exists(config_file):
            configs = parse_json_config(config_file)
            mariadbHandler = MariaDBHandler(configs)


        else:
            print(f'Cannot find config file: {config_file}')

    except Exception as e:
        print(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")