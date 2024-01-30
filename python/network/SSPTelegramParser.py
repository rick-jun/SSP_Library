from struct import *
from datetime import datetime
from SSPUtils import parse_json_config
import sys

class SSPTelegramParser:
    #========================================================================================    
    @property
    def header_format(self):
        return self._header_format

    @property
    def header_length(self):
        return self._header_length
    
    @property
    def bodies(self):
        return self._bodies
    #========================================================================================       
    def __init__(self, logger) -> None:
        try:     
            self.logger = logger  

            self.logger.info(f"Start parsing telegrams.json file.")

            self.configs = parse_json_config('telegrams.json')

            self._header_format = self.configs["header"]["f_string"]
            self._header_length = self.configs["header"]["length"]
            self._bodies = {}

            for _, value in self.configs["bodies"].items():
                b = Body(value)
                self._bodies[b.code] = b   
            
        except Exception as e:
            self.logger.error(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")
    #========================================================================================
    def get_body_obj(self, input):
        """
        input can be a telegram code (int) or header (byte[])

        return f_string, length
        """
        try:
            body_obj = None

            if isinstance(input , bytes):
                # parse header to extract code
                input = int(unpack(self.header_format, input)[1])

            if input in self._bodies:
                body_obj = self._bodies[input]

        except Exception as e:
            self.logger.error(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")

        return body_obj
    #========================================================================================
    def parse_header(self, input):
        """
        input can be a telegram code (int) or header (byte[])

        return code,  dTime
        """
        try:
            # parse header
            header_data = unpack(self.header_format, input)

            stx = header_data[0]
            length = header_data[1]
            request_code = header_data[2]
            dummy1 = header_data[3]
            dummy2 = header_data[4]

            if stx != b'\x02' or length != b'\x1A' or dummy1 != b'\x00' or dummy2 != b'\x00':
                return False, header_data

        except Exception as e:
            self.logger.error(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")

        return True, header_data
    #========================================================================================
    def create_packet(self, body, *args):
        """
        Parameters:
            body: Body object
            *args: data needed to create corresponding telegram.

        return byte[]
        """

        try:
            current_datetime = datetime.now()
            header = pack(self._header_format, 
                          b"POSR", 
                          body.code,  
                          current_datetime.year,
                          current_datetime.month,
                          current_datetime.day,
                          current_datetime.hour,
                          current_datetime.minute,
                          current_datetime.second,
                          current_datetime.microsecond//1000
                          )
            try:
                body_data = pack(body.f_string, *args)

                return header + body_data
            except Exception as e:
                self.logger.error(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}] while packing body data: {e}")

                return None
            
        except Exception as e:
            self.logger.error(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")

            return None
    #========================================================================================

###################################################################################################
class Body:
        
    def __init__(self, jdata) -> None:
        self._f_string = jdata["f_string"]
        self._length = jdata["length"]
    #========================================================================================
    @property
    def f_string(self):
        return self._f_string
    
    @property
    def length(self):
        return self._length
    
    #========================================================================================