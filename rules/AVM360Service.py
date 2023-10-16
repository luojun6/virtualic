
import threading
from IPython.core.display import display
from common.ipywidgetsUtilities import get_output_model_id
from components.AVM360Page import AVM360Page
from components.VirtualSystem import VituralSystemContext
from components.SignalClusters_AVM360 import SignalClusterAVM360
from components.PMIC_AVM360 import PowerControlBox_AVM360

from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)
    
    
class AVM360Context(VituralSystemContext):
    
    # def __init__(self, headunit: VirtualHeadUnit):
    def __init__(self):
        # self.__display = self.system.display
        super().__init__()
        self.__avm360page = AVM360Page()
        
        self.__signal_cluster = SignalClusterAVM360()
        self.__pmic = PowerControlBox_AVM360()
        
        self.__dock_entered = threading.Event()
        
        self.__register_callbacks()
        
    def __register_callbacks(self):
        self.__avm360page.home_button.on_click(self.__exit_avm360page)
        
    def __exit_avm360page(self, button):
        self.system.dock_context.enter_home_page()
        self.__dock_entered.clear()
        self.avm360page.clear_setting()
        
    def power_on(self):
        self.__pmic.power_on()
        
    def power_off(self):
        self.__pmic.power_off()    
    
    @property
    def pmic(self):
        return self.__pmic
        
    @property
    def signal_cluster(self):
        return self.__signal_cluster
        
    @property
    def avm360page(self):
        return self.__avm360page    
    
    def dock_entered(self):
        self.__dock_entered.set()
        self.enter_avm360page()
    
    def enter_avm360page(self):
        if get_output_model_id(self.system.display.foreground) != self.__avm360page.model_id:
        
            with self.system.display.foreground:
                display(self.__avm360page)
                
        else:
            _logger.error("Already in avm360page!")
    
    # def __on_change_gear_sts(self, change):
    #     new_value = change["new"]
    #     signal = self.__signal_cluster.gear_sts.signal
        
    #     if new_value == signal.ReverseRange.value:
    #         self.__enter_avm360page()
            
    # def __enter_avm360page(self):
    #     if not self.__on_avm360page:
    #         self.__display.clear_all_output()
            
    #         with self.__display.foreground:
    #             display(self.__avm360page)
                


avm360context = AVM360Context()