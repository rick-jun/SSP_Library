import paho.mqtt.client
from paho.mqtt.properties import Properties as Properties
import paho.mqtt.publish as publish
import time

class MQClient(paho.mqtt.client.Client):
    """
    """

    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60

    _topic = None
    _qos = None

    #------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #------------------------------------------------------------------------------
    def on_disconnect(self, client, userdata, rc):

        reconnect_count, reconnect_delay = 0, self.FIRST_RECONNECT_DELAY
        while reconnect_count < self.MAX_RECONNECT_COUNT:
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                return
            except Exception as e:
                print(e)

            reconnect_delay *= self.RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, self.MAX_RECONNECT_DELAY)
            reconnect_count += 1

    #------------------------------------------------------------------------------
    def set_topic(self, input):
        if isinstance(input, tuple):
            self._topic = input[0]
            self._qos = input[1]
        elif isinstance(input, str):
            self._topic = input

    #------------------------------------------------------------------------------
    def short_publish(self, message, qos=0):
        if self._topic is not None:
            returnvalue = self.publish(self._topic, message)
            if qos == 2 or self._qos == 2:
                self.loop()                
            return returnvalue
        return None
    
#====================================================================================================
if __name__ == '__main__':
    mqtt_client = MQClient.Client()    

    count = 50

    while count > 0:
        time.sleep(1)
        count -= 1
    
