# import ipywidgets as widgets

from components.DisplayPanel import DisplayPanel
# from components.SignalClusters import SignalClusterPM
# from rules.HeadUnitPM import PowerManagementDisplay as HeadUnitPM
from components.VirtualSystem import VirtualSystem
from rules.VehicleHeadUnitPM import VehicleHeadUnitPM_SAIC
from rules.DockEvents import DockContext
from rules.SRV360Service import SRV360Context


from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)




class VirtualSystem_HeadUnit(VirtualSystem):

    def __init__(self,
                 display: DisplayPanel,
                 veh_hu_pm: VehicleHeadUnitPM_SAIC):
        super(VirtualSystem_HeadUnit, self).__init__()
        
        self.__display = display
        self.__veh_hu_pm = veh_hu_pm
        self.__dock_context = DockContext()
        self.__srv360context = SRV360Context()
        
        self.__conext_list = list()
        self.__start_context()
        
        self.__veh_hu_pm.set_veh_power_on_callback(self.__veh_power_on_callback)
        self.__veh_hu_pm.set_veh_power_off_callback(self.__veh_power_off_callback)
    
    
    def __veh_power_on_callback(self):
        _logger.debug("Executing __veh_power_on_callback().")
        # self.__start_context()
        
        for context in self.__conext_list:
            
            if "power_on" in dir(context):
                context.power_on()
        
    def __veh_power_off_callback(self):
        _logger.debug("Executing __veh_power_off_callback().")
        self.__power_off_context()
        
        
    def __start_context(self):
        
        self.__conext_list.append(self.__dock_context)
        self.__conext_list.append(self.__srv360context)
        
        for context in self.__conext_list:
            context.system = self   
            
 
    def __power_off_context(self):
        for context in self.__conext_list:
            if "power_off" in dir(context):
                context.power_off()
        
        
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
    def srv360context(self):
        return self.__srv360context    


