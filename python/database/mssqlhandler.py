import sys
import pyodbc
import pandas as pd

from ssp.loghelpers import LogLelvel

class MSSQLHandler:

    #========================================================================================
    def __init__(self, id, log_publisher, configs):
        self.id = id
        self.configs = configs
        self._log_publisher = log_publisher

        self._log_publisher.pub_log("Creating DBHandler...")

        self.isConnected = self.connect_to_sql_server()
    #========================================================================================
    def connect_to_sql_server(self):

        connection_string = f"DRIVER={{SQL Server}};SERVER={self.configs['host']};DATABASE={self.configs['db_name']};UID={self.configs['username']};PWD={self.configs['password']}"

        try:
            # Establish the connection
            self.connection = pyodbc.connect(connection_string)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self._log_publisher.pub_log("Connected to SQL Server")   
            return True

        except pyodbc.Error as e:
            self._log_publisher.pub_log("Cannot connect to DB.", LogLelvel.ERROR)
            self._log_publisher.pub_log(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}", LogLelvel.ERROR)
            return False
    #========================================================================================
    @property
    def IsConnected(self):
        return self.isConnected
    #========================================================================================
    def get_single_value(self, query):
        try:
            return self.cursor.execute(query).fetchval()
        except Exception as e:
            self._log_publisher.pub_log("Error while executing query: " + query, LogLelvel.ERROR)
            self._log_publisher.pub_log(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}", LogLelvel.ERROR)
    #========================================================================================
    def get_values(self, query):
        try:
            return self.cursor.execute(query).fetchone()
        except Exception as e:
            self._log_publisher.pub_log("Error while executing query: " + query, LogLelvel.ERROR)
            self._log_publisher.pub_log(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}", LogLelvel.ERROR)
            
    #========================================================================================
    def get_df(self, query):
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            data = [list(t) for t in data]
            columns = [column[0] for column in self.cursor.description]
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            self._log_publisher.pub_log("Error while executing query: " + query, LogLelvel.ERROR)
            self._log_publisher.pub_log(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}", LogLelvel.ERROR)

    #========================================================================================
    def update_status(self, tablename, robotid, update_dic):
        try:

            query = f"UPDATE {tablename} SET timestamp = GETDATE() "

            for key, value in update_dic.items():
                query += f" , {key} = '{value}'"
            
            query += f" WHERE RobotID = {robotid}"

            self.cursor.execute(query)

        except Exception as e:
            self._log_publisher.pub_log(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}", LogLelvel.ERROR)
            
    #========================================================================================
    def update_single_status(self, tablename, robotid, column, value):
        try:
            query = f"UPDATE {tablename} SET timestamp = GETDATE() "

            query += f" , {column} = '{value}'"
            
            query += f" WHERE RobotID = {robotid}"

            self.cursor.execute(query)

        except Exception as e:
            self._log_publisher.pub_log(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}", LogLelvel.ERROR)

    #========================================================================================
    def __del__(self):        
        try:
            # Close the connection
            if hasattr(self, "connection"):
                self.connection.close()
        except Exception as e:       
            self._log_publisher.pub_log(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}", LogLelvel.ERROR)
        finally:
            self._log_publisher.pub_log("DBHandler terminated.")
    #========================================================================================
# end of DBHandler
