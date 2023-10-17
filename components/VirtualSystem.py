import threading
# import ipywidgets as widgets

class VirtualSystem(threading.Thread):
    def __init__(self):
        super(VirtualSystem, self).__init__()

class VituralSystemContext(threading.Thread):
    def __init__(self):
        super(VituralSystemContext, self).__init__()
        self.__enabled = threading.Event()
        
    @property
    def system(self):
        return self.__system
    
    @system.setter
    def system(self, deployed_system):
        self.__system = deployed_system
        self.register_callbacks()
        
    def register_callbacks(self):
        pass
    
    def enable_context(self):
        self.__enabled.set()
        
    def disable_context(self):
        self.__enabled.clear()
        
    @property
    def context_enabled(self):
        return self.__enabled.is_set()