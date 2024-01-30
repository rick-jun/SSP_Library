import sys
import socket
import random
from logging.handlers import TimedRotatingFileHandler, QueueHandler
import logging
from ssp.confighandler import parse_json_config

def get_available_port(ip='127.0.0.1', port_range_start=1024, port_range_end=65535):
    """
    Returns available port number on the machine.

    Parameters:
        ip = IP address to bind the socket
        port_range_start = smallest value of possible port number
        port_range_end = largest value of possible port number

    Return:
        a single integer of port number
    """
    # Generate a random port number between port_range_start and port_range_end
    random_port = random.randint(port_range_start, port_range_end)

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Attempt to bind the socket to the local host and random port
        server_socket.bind((ip, random_port))
        server_socket.close()  # Close the socket
        return random_port
    except socket.error:
        # If binding fails (port is already in use), try again
        return get_available_port(ip, port_range_start, port_range_end)
#========================================================================================
def get_multiprocessing_logger(name, log_queue):
    """
    creates logger with QueueHandler

    Parameters:
        name = name of the logger
        log_queue = shared multiprocessing.Queue()

    Returns:
        logger
    """
    # create logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
        handlers=[QueueHandler(log_queue)]     
    )

    return logging.getLogger(name)
#====================================================================================================
def multiprocessing_logger_process(queue, logfile_fullpath):
    """
    Writes message in shared multiprocessing.Queue() to log target.

    Parameters:
        queue = shared multiprocessing.Queue()
        configs = JSon config object

    """
    try:
        # create logger
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s\t[%(levelname)s]\t%(name)-20s%(message)s',
            handlers=[
                TimedRotatingFileHandler(filename=logfile_fullpath, when='midnight', interval=1, backupCount=10),
                logging.StreamHandler()
            ]     
        )
        logger = logging.getLogger()

        # run forever
        while True:
            # consume a log message, block until one arrives
            log_message = queue.get()
            # check for shutdown
            if log_message is None:
                break
            # log the message
            logger.handle(log_message)
    except KeyboardInterrupt:
        queue.empty()
        print("Received a keyboard interrupt. Terminating multiprocessing_logger_process().")
    except Exception as e:
        logger.error(f"Error at [{__name__}], FunctionName=[{sys._getframe().f_code.co_name}]: {e}")
    finally:
        queue = None
#====================================================================================================
