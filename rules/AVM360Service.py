
import threading
from IPython.core.display import display
from components.AVM360Page import avm360page
# from components.VirtualHeadUnit import VirtualHeadUnit
from components.SignalClusters_AVM360 import SignalClusterAVM360
from components.PMIC_AVM360 import PowerControlBox_AVM360


    
    
class AVM360Service(threading.Thread):
    
    # def __init__(self, headunit: VirtualHeadUnit):
    def __init__(self, headunit):
        self.__display = headunit.display
        self.__avm360page = avm360page
        
        self.__signal_cluster = SignalClusterAVM360()
        self.__pmic = PowerControlBox_AVM360()
        
        self.__dock_entered = threading.Event()
        self.__on_avm360page = threading.Event()
        
        self.__signal_cluster.gear_sts.set_on_change_callback(self.__on_change_gear_sts)
        
    @property
    def signal_cluster(self) -> SignalClusterAVM360:
        return self.__signal_cluster
        
    @property
    def dock_entered(self) -> threading.Event:
        return self.__dock_entered
    
    @property
    def on_avm360page(self) -> threading.Event:
        self.__on_avm360page
        
    @property
    def avm360page(self):
        return self.__avm360page    
    
    def __on_change_gear_sts(self, change):
        new_value = change["new"]
        signal = self.__signal_cluster.gear_sts.signal
        
        if new_value == signal.ReverseRange.value:
            self.__enter_avm360page()
            
    def __enter_avm360page(self):
        if not self.__on_avm360page:
            self.__display.clear_all_output()
            
            with self.__display.forground:
                display(self.__avm360page)
                

