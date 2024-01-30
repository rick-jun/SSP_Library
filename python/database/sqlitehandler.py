import sqlite3
import sys

class SQLiteHandler :

    def __init__(self, src):

        self._src = src

    def selModel(self) :
        try :
           
            db = sqlite3.connect(self._src)
            cur = db.cursor()

            cur.execute("SELECT id, name, ScriptPath, WeightPath FROM models")
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result = []
            for row in rows :
                row = dict(zip(columns, row))
                result.append(row)

            db.close()

            return result

        except :

            print('DB 연결 실패')
            return None
        
    def selResultLabels(self) :
        try :
           
            db = sqlite3.connect(self._src)
            cur = db.cursor()

            cur.execute("SELECT id, localizedName FROM resultLabels")
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result = []
            for row in rows :
                row = dict(zip(columns, row))
                result.append(row)

            db.close()

            return result

        except :

            print('DB 연결 실패')
            return None

            

    def selChoosenConfig(self, id) :
        try :
           
            db = sqlite3.connect(self._src)
            cur = db.cursor()
            
            cur.execute("SELECT * FROM configs where id = {}".format(id))
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result = []
            for row in rows :
                row = dict(zip(columns, row))
                result.append(row)

            
            db.close()

            return result

        except :

            print('DB 연결 실패')

            return "Fail"
        
    def selConfig(self) :
        try :
           
            db = sqlite3.connect(self._src)
            cur = db.cursor()

            cur.execute("SELECT * FROM configs")
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result = []
            for row in rows :
                row = dict(zip(columns, row))
                result.append(row)

            db.close()

            return result

        except :

            print('DB 연결 실패')

            return "Fail"

    def editConfig(self, data) :
        try :
            
            rcvdata = (data['id'], data['title'], data['cctvUrl'], data['aiModelID'], data['alarm1_on_Url'], data['alarm1_off_Url'], data['alarm2_on_Url'], data['alarm2_off_Url'], data['requiredAlarmFrame'], data['alarmThreshold'], data['alarmResultLabel'], data['confidenceObject'], data['alarm3_on_Url'], data['alarm3_off_Url'], data['alarm4_on_Url'], data['alarm4_off_Url'])
            
            db = sqlite3.connect(self._src)
            cur = db.cursor()
            
            cur.execute(f"SELECT COUNT(*) AS cnt FROM configs WHERE id='{data['id']}'")
            rows = cur.fetchall()
            
            if rows[0][0] == 1 :
                
                query = f"UPDATE configs SET id=?, title=?, cctvUrl=?, aiModelID=?, alarm1_on_Url=?, alarm1_off_Url=?, alarm2_on_Url=?, alarm2_off_Url=?, requiredAlarmFrame=?, alarmThreshold=?, alarmResultLabel=?, confidenceObject=?, alarm3_on_Url=?, alarm3_off_Url=?, alarm4_on_Url=?, alarm4_off_Url=? WHERE id = {data['id']};"
                
                
                cur.execute(query, rcvdata)

            elif rows[0][0] == 0 :

                query = "INSERT INTO configs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                
                cur.execute(query, rcvdata)

            db.commit()

            db.close()

            return "Success"

        except :

            print('DB 연결 실패')

            return "Fail"

    def delConfig(self, data) :
        try :
            
            db = sqlite3.connect(self._src)
            cur = db.cursor()
            delquery = "DELETE FROM configs WHERE id =?"
            cur.execute(delquery, data)

            db.commit()
            db.close()

            return "Success"

        except :

            print('DB 연결 실패')
            
            return "Fail"
        
    def selMaxConfig(self) :
        try :
           
            db = sqlite3.connect(self._src)
            cur = db.cursor()

            cur.execute("SELECT Max(id) AS max FROM configs")
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result = []
            for row in rows :
                row = dict(zip(columns, row))
                result.append(row)

            db.close()

            return result

        except :

            print('DB 연결 실패')

    def selAlarm(self, configID) :
        try :
           
            db = sqlite3.connect(self._src)
            cur = db.cursor()

            cur.execute(f"SELECT * FROM alarms where configID={configID} order by start desc limit 100;")
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result = []
            for row in rows :
                row = dict(zip(columns, row))
                result.append(row)

            db.close()

            return result

        except :

            print('DB 연결 실패')

    def selDupAlarm(self, data, configID) :
        try :
           
            db = sqlite3.connect(self._src)
            cur = db.cursor()
            
            cur.execute(f"SELECT count(*) FROM alarms where start = '{data['start']}' AND end = '-' AND configID = {configID} ;")
            
            rows = cur.fetchall()
            #print(rows[0][0])
            db.close()

            return rows[0][0]

        except :

            print('DB 연결 실패')
            return -1
        
    def insertAlarm(self, data, configID) :
        try :
            imagepath = "D:/AlarmImages/"+configID+"/"+data['start']
            rcvdata = (data['start'], data['end'], configID, imagepath, data['confidence'])
            
            db = sqlite3.connect(self._src)
            cur = db.cursor()

            query = "INSERT INTO alarms (start, end, configid, image_path, confidence) VALUES (?,?,?,?,?);"
            #print(query)
            cur.execute(query, rcvdata)

            db.commit()

            db.close()

            return "Success"

        except :

            print('DB 연결 실패')

            return "Fail"
        

    def insertAlarmImages(self, data) :
        try :
            rcvdata = (data['configid'], data['start'], data['image_path'], data['confidence'])
            
            db = sqlite3.connect(self._src)
            cur = db.cursor()

            query = "INSERT INTO alarmImages (configid, start, image_path, confidence) VALUES (?,?,?,?);"
            
            #print(query)
            cur.execute(query, rcvdata)

            db.commit()

            db.close()

            return "Success"

        except Exception as e:
            print(f"Error at [{self.__class__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")          

            return "Fail"
        
    def updateAlarm(self, data, configID) :
        try :

            db = sqlite3.connect(self._src)
            cur = db.cursor()

            query = f"UPDATE alarms SET end='{data['end']}', confidence={data['confidence']} WHERE start = '{data['start']}' AND configID = {configID};"
            #print(query)
            cur.execute(query)
            
            db.commit()

            db.close()

            return "Success"

        except :

            print('DB 연결 실패')

            return "Fail"
