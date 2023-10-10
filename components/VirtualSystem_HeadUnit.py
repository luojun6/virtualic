# import ipywidgets as widgets

from components.DisplayPanel import DisplayPanel
# from components.SignalClusters import SignalClusterPM
# from rules.HeadUnitPM import PowerManagementDisplay as HeadUnitPM
from rules.VehicleHeadUnitPM import VehicleHeadUnitPM

# import rules.DockEvents as dock
# import rules.AVM360Service as avm360

# from utils.loggers import Logger, logging_handler
# import logging

# _logger = Logger(logger_name=__file__,
#                  log_handler=logging_handler,
#                  logging_level=logging.DEBUG)


from components.VirtualSystem import VirtualSystem, VituralSystemContext

class VirtualSystem_HeadUnit(VirtualSystem):

    def __init__(self,
                 display: DisplayPanel,
                 veh_hu_pm: VehicleHeadUnitPM,
                 dock_context: VituralSystemContext,
                 avm360context: VituralSystemContext):
        super(VirtualSystem_HeadUnit, self).__init__()
        
        self.__display = display
        self.__veh_hu_pm = veh_hu_pm
        self.__dock_context = dock_context
        self.__avm360context = avm360context
        
        self.__conext_list = list()
        self.__init_context()

        
    def __init_context(self):
        
        self.__conext_list.append(self.__dock_context)
        self.__conext_list.append(self.__avm360context)
        
        for context in self.__conext_list:
            context.system = self
    #         context.start()     
        
    # def stop_context(self):
    #     for context in self.__conext_list:
    #         context.join()
        
    @property
    def display(self):
        return self.__display
    
    @property
    def veh_hu_pm(self):
        return self.__veh_hu_pm
    
    @property
    def dock_context(self):
        return self.__dock_context
    
    @property
    def avm360context(self):
        return self.__avm360context
    
    
    


