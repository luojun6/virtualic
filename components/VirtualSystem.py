import threading
# import ipywidgets as widgets

class VirtualSystem(threading.Thread):
    def __init__(self):
        super(VirtualSystem, self).__init__()

class VituralSystemContext(threading.Thread):
    def __init__(self):
        super(VituralSystemContext, self).__init__()
        self.__is_enabled = threading.Event()
        
    @property
    def system(self):
        return self.__system
    
    @system.setter
    def system(self, deployed_system):
        self.__system = deployed_system
        self.register_callbacks()
        
    def register_callbacks(self):
        pass
    
    def enable(self):
        self.__is_enabled.set()
        
    def disable(self):
        self.__is_enabled.clear()
        
    @property
    def is_enabled(self):
        return self.__is_enabled.is_set()