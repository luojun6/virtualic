import ipywidgets as widgets

from components.DisplayPanel import DisplayPanel
from components.SignalClusters import SignalClusterPM
from components.VirtualSystem_HeadUnit import VirtualSystem_HeadUnit
from rules.HeadUnitPM import PowerManagementDisplay as HeadUnitPM
from rules.VehicleHeadUnitPM import VehicleHeadUnitPM_SAIC


class HeadUnit_AVM360(widgets.HBox):
    def __init__(self):
        self.__display = DisplayPanel()
        self.__signal_cluster_pm = SignalClusterPM()
        self.__hu_pm = HeadUnitPM(display=self.__display)
        self.__veh_hu_pm = VehicleHeadUnitPM_SAIC(hu_pm=self.__hu_pm, sc_pm=self.__signal_cluster_pm)
        self.__hu = VirtualSystem_HeadUnit(display=self.__display, veh_hu_pm=self.__veh_hu_pm)
        super().__init__(
            children=[self.__hu.display, self.__hu.avm360context.pmic]
        )
        self.layout = widgets.Layout(justify_content="space-around")
    
    @property
    def headunit(self):
        self.__hu