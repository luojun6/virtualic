
from abc import ABC, abstractmethod
from IPython.core.display import display
from components.AVM360Page import AVM360Page
import components.ForgroundPages as pages
from components.DisplayPanel import DisplayPanel
from components.SignalClusters import SignalClusterPM
from components.SignalClusters_AVM360 import SignalClusterAVM360
from components.PMIC_AVM360 import PowerControlBox_AVM360


    
    
class AVM360Context:
    
    def __init__(self, display: DisplayPanel, avm360page: AVM360Page, veh_pm_signal_cluster: SignalClusterPM):
        self.__display = display
        self.__avm360page = avm360page
        self.__veh_pm_signal_cluster = veh_pm_signal_cluster
        
        self.__signal_cluster = SignalClusterAVM360()
        self.__pmic = PowerControlBox_AVM360()
        
        self.__dock_entered = False
        self.__on_avm360page = False
        
        self.__signal_cluster.gear_sts.set_on_change_callback(self.__on_change_gear_sts)
        
    @property
    def signal_cluster(self) -> SignalClusterAVM360:
        return self.__signal_cluster
        
    @property
    def dock_entered(self) -> bool:
        return self.__dock_entered
    
    @dock_entered.setter
    def dock_entered(self, value: bool):
        self.__dock_entered = value
        
    @property
    def on_avm360page(self) -> bool:
        self.__on_avm360page
        
    @on_avm360page.setter
    def on_avm360page(self, value: bool):
        self.__on_avm360page = value
        
    @property
    def avm360page(self) -> AVM360Page:
        return self.__avm360page    
    
    def __on_change_gear_sts(self, change):
        new_value = change["new"]
        signal = self.__signal_cluster.gear_sts.signal
        
        if new_value == signal.ReverseRange.value:
            self.__enter_avm360page()
    
    def __clear_display_output(self):
        self.__display.dock.clear_output()
        self.__display.forground.clear_output()
            
    def __enter_avm360page(self):
        if not self.__on_avm360page:
            self.__clear_display_output()
            
            with self.__display.forground:
                display(self.__avm360page)
                

