import ipywidgets as widgets

from components.DisplayPanel import DisplayPanel
from components.SignalClusters import SignalClusterPM
from components.VirtualSystem_HeadUnit import VirtualSystem_HeadUnit
from rules.HeadUnitPM import PowerManagementDisplay as HeadUnitPM
from rules.VehicleHeadUnitPM import VehicleHeadUnitPM_SAIC


class HeadUnit_AVM360(widgets.VBox):
    ROW_LAYOUT = widgets.Layout(justify_content="space-around")
    def __init__(self):
        self.__display = DisplayPanel()
        self.__signal_cluster_pm = SignalClusterPM()
        self.__hu_pm = HeadUnitPM(display=self.__display)
        self.__veh_hu_pm = VehicleHeadUnitPM_SAIC(hu_pm=self.__hu_pm, sc_pm=self.__signal_cluster_pm)
        self.__hu = VirtualSystem_HeadUnit(display=self.__display, veh_hu_pm=self.__veh_hu_pm)
        self.layout = self.ROW_LAYOUT
        super().__init__(
            children=[
                widgets.HBox(children=[self.__hu.display, self.__hu.avm360context.pmic], layout=self.ROW_LAYOUT), 
                # self.__veh_hu_pm.signal_cluster
                ]
        )
   
    
    @property
    def hu(self):
        return self.__hu
        
    # @property
    # def veh_pm_signal_cluster(self):
    #     return 