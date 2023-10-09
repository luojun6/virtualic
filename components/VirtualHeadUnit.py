import ipywidgets as widgets

from components.DisplayPanel import DisplayPanel
from components.SignalClusters import SignalClusterPM
from rules.HeadUnitPM import PowerManagementDisplay as HeadUnitPM
from rules.VehicleHeadUnitPM import VehicleHeadUnitPM_SAIC

import rules.DockEvents as dock
import rules.AVM360Service as avm360

# from utils.loggers import Logger, logging_handler
# import logging

# _logger = Logger(logger_name=__file__,
#                  log_handler=logging_handler,
#                  logging_level=logging.DEBUG)


class VirtualHeadUnit(widgets.VBox):

    def __init__(self,
                 display_class=DisplayPanel,
                 headunit_pm_class=HeadUnitPM,
                 pm_signals_class=SignalClusterPM,
                 veh_pm_class=VehicleHeadUnitPM_SAIC,
                 avm360service_class=avm360.AVM360Service,
                 dock_context_class=dock.DockContext,
                 **kwargs):

        self.__display = display_class()
        self.__hu_pm = headunit_pm_class(display=self.__display)
        self.__sc_pm = pm_signals_class()
        self._veh_headunit_pm = veh_pm_class(
            hu_pm=self.__hu_pm, sc_pm=self.__sc_pm)
        if self._veh_headunit_pm.headunit_pm.display != self.__display:
            raise ValueError(
                f"The display of power_manager is not the instance of {self.__class__.__name__}!")
        self.__avm360service = avm360service_class(headunit=self)
        self.__dock_context = dock_context_class(headunit=self)
        if self.__dock_context.display != self.__display:
            raise ValueError(
                f"The display of dock_context is not the instance of {self.__class__.__name__}!")

        super().__init__(
            children=[self.__display, self._veh_headunit_pm.signal_cluster], **kwargs)
        
    @property
    def display(self):
        return self.__display
    
    @property
    def dock_context(self):
        return self.__dock_context
    
    @property
    def avm360service(self):
        return self.__avm360service
    


