"""
Update history

20240105 - Rick: Replaced MQData class to use configs.json

"""

import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler, QueueHandler
from dataclasses import dataclass
from enum import Enum, unique

from ssp.mqclient import MQClient
#====================================================================================================
@unique
class LogLelvel(Enum):
    INFO = 0
    ERROR = 1
    DEBUG = 2

#=====================================================================================================
class LogSubscriber:
    '''
    Gets log message from MQTT and write to a log file.
    Log file lotation can be enabled.

    '''

    _isready = False
    _configs = None
    _logfile_fullpath = ""
    _logger = None
    _mqtt_client = None
    _broker_ip = "localhost"
    _broker_port = 1883
    _topic = None
    _mq_qos  = 0

    @property
    def IsReady(self):
        return self._isready
    
    #----------------------------------------------------------------------------------------------------
    def __init__(self, conf, subtopic="#"):
        '''        
        Parameter:
            config: config dictionary
            topic: MQTT topic to listen
        '''
        try:
            self._configs = conf
            self._mq_broker_ip = self._configs["MQ"]["BrokerIP"]
            self._mq_broker_port = self._configs["MQ"]["BrokerPort"]
            self._mq_broker_qos = self._configs["Logging"]["QoS"]
            
            self._topic = f'{self._configs["Logging"]["LogTopic"]}/{subtopic}'

            self._logfile_fullpath = os.path.join(self._configs["Logging"]["log_folder"], self._configs["Logging"]["log_file_basename"])

            # create logger
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s\t[%(levelname)s]%(message)s', # message will be "\t%(name)-30s%(message)s"                
                handlers=[
                    TimedRotatingFileHandler(filename=self._logfile_fullpath, when='midnight', interval=1, backupCount=self._configs["Logging"]["number_of_logfiles_to_keep"]),
                    logging.StreamHandler()
                ]     
            )
            self._logger = logging.getLogger()

            self._mqtt_client = MQClient()
            self._mqtt_client.connect(self._broker_ip, self._broker_port)
            msginfo = self._mqtt_client.subscribe(self._topic, qos=self._mq_qos)
            # print(f'topic: {self._topic}, msginfo: {msginfo}')
            self._mqtt_client.on_message = self._on_message

            self._isready = True

            print(f"LogSubscriber listening on topic {self._topic} created.")
        except Exception as e:
            print(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")

    #----------------------------------------------------------------------------------------------------
    def loop_start(self):
        if self._isready:
            self._mqtt_client.loop_start()
            return True
        else:
            return False
        
    #----------------------------------------------------------------------------------------------------
    def _on_message(self, client, userdata, msg):
        # print("LogHandler _on_message triggered.")
        try:
            # name/level
            name = msg.topic.split('/')[-2]
            level = msg.topic.split('/')[-1]
            message = f'\t{name:<20}{msg.payload.decode()}'

            # print(f'_on_message message: {message}')
            if level == str(LogLelvel.INFO.value):
                self._logger.info(message)
            elif level == str(LogLelvel.DEBUG.value):
                self._logger.debug(message)
            elif level == str(LogLelvel.ERROR.value):
                self._logger.error(message)

        except Exception as e:
            print(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")
            
    #----------------------------------------------------------------------------------------------------

#=====================================================================================================
class LogPublisher:

    _configs = None
    _mqtt_log_pub_topic_base = None

    #----------------------------------------------------------------------------------------------------
    def __init__(self, config, subtopic="", trace=False):
        try:
            self._configs = config
            self._mq_broker_ip = self._configs["MQ"]["BrokerIP"]
            self._mq_broker_port = self._configs["MQ"]["BrokerPort"]
            self._mq_broker_qos = self._configs["Logging"]["QoS"]
            self._mqtt_log_pub = MQClient()
            self._mqtt_log_pub.connect(self._mq_broker_ip, self._mq_broker_port)
            

            self._mqtt_log_pub_topic_base = self._configs["Logging"]["LogTopic"]
            if subtopic != "":
                self._mqtt_log_pub_topic_base = f'{self._mqtt_log_pub_topic_base}/{subtopic}'

            if trace:
                print(f"LogPublisher {subtopic} created.")
        except Exception as e:
            print(f"Error at [{self.__class__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")
            
    #----------------------------------------------------------------------------------------------------
    def pub_log(self, msg, level=LogLelvel.INFO):
        try:
            # print(f'_log_pub triggered. topic: {self._mqtt_log_pub_topic_base}')
            # msginfo = self._mqtt_log_pub.publish(self._mqtt_log_pub_topic_base + '/' + str(level.value), msg, qos)
            # print(msginfo)
            rt, mid = self._mqtt_log_pub.publish(self._mqtt_log_pub_topic_base + '/' + str(level.value), msg, self._mq_broker_qos)

            if self._mq_broker_qos == 2:
                self._mqtt_log_pub.loop()

        except Exception as e:
            print(f"Error at [{self.__class__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")

    #----------------------------------------------------------------------------------------------------
    

#=====================================================================================================
