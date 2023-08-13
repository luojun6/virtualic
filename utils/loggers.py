#!/bin/python3

# import os, sys
# current_dir = os.path.dirname(__file__)
# root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.insert(0, root_dir)


import ipywidgets as widgets
from IPython.display import display
import logging

class Logger:
    def __init__(self, logger_name="DefaultLogger", 
                 log_handler=logging.StreamHandler(),
                 logging_level=logging.DEBUG):
        self.__logger = logging.getLogger(logger_name)
        if logging_level not in logging._levelToName:
            raise TypeError(f"Invalid input logging_level: {logging_level}.")
        self.__logger.setLevel(logging_level)
        self.__ch = log_handler
        self.__ch.setLevel(logging_level)
        
        self.__formatter = logging.Formatter(
            f'%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
        self.__ch.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__ch)
        
    def debug(self, msg):
        self.__logger.debug(msg)
        
    def info(self, msg):
        self.__logger.info(msg)
        
    def warn(self, msg):
        self.__logger.warning(msg)
        
    def error(self, msg):
        self.__logger.error(msg)
        
    def critical(self, msg):
        self.__logger.critical(msg)
    
    
class OutputWidgetHandler(logging.Handler):
    """ Custom logging handler sending logs to an output widget """

    def __init__(self, *args, **kwargs):
        super(OutputWidgetHandler, self).__init__(*args, **kwargs)
        layout = {
            'width': '100%',
            'height': 'auto',
            'border': '1px solid black'
        }
        self.out = widgets.Output(layout=layout)

    def emit(self, record):
        """ Overload of logging.Handler method """
        formatted_record = self.format(record)
        new_output = {
            'name': 'stdout',
            'output_type': 'stream',
            'text': formatted_record+'\n'
        }
        self.out.outputs = (new_output, ) + self.out.outputs

    def show_logs(self):
        """ Show the logs """
        display(self.out)

    def clear_logs(self):
        """ Clear the current logs """
        self.out.clear_output()
        

logging_handler = OutputWidgetHandler()
        
if __name__ == "__main__":
    print(logging.DEBUG in logging._levelToName)
        
