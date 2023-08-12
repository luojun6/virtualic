#!/bin/python3

# import os, sys
# current_dir = os.path.dirname(__file__)
# root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.insert(0, root_dir)

import threading
import logging
_logger = logging.getLogger(__file__)
_logger.setLevel(logging.DEBUG)

_ch = logging.StreamHandler()
_ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_ch.setFormatter(formatter)
_logger.addHandler(_ch)


class SafeThread(threading.Thread):
    def __init__(self, name=None, logger=_logger):
        super(SafeThread, self).__init__()
        self.__name = self.__class__.__name__
        self.logger = logger
        
        self.__flag = threading.Event() # Used to pause threading
        self.__flag.set() # Set as True
        self.__running = threading.Event() # Used to stop threading
        self.__running.set()

    def run(self):
        self.logger.debug(f"{self.name}: {self.__name} starts running.")

    def is_running(self):
        return self.__running.isSet()

    def is_waiting_for_pause(self):
        return self.__flag.wait()

    def pause(self):
        self.__flag.clear() # Set as False to pause threading

    def resume(self):
        self.__flag.set() # Set as True to resume threading

    def stop(self):
        self.__flag.set()
        self.__running.clear()
        self.join()
        self.logger.debug(f"{self.name}: {self.__name} has been stopped.")


if __name__ == "__main__":
    import time

    st = SafeThread()
    st.start()
    time.sleep(3)
    st.stop()