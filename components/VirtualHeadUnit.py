import ipywidgets as widgets

from components.DisplayPanel import DisplayPanel
from components.SignalClusters import SignalClusterPM
from components.AVM360Page import AVM360Page
from rules.HeadUnitPM import PowerManagementDisplay as HeadUnitPM
from rules.VehicleHeadUnitPM import VehicleHeadUnitPM_SAIC
import rules.DockEvents as dock

from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)


class VirtualHeadUnit(widgets.VBox):

    def __init__(self,
                 display_class=DisplayPanel,
                 headunit_pm_class=HeadUnitPM,
                 pm_signals_class=SignalClusterPM,
                 veh_pm_class=VehicleHeadUnitPM_SAIC,
                 avm360pager_class=AVM360Page,
                 dock_context_class=dock.DockContext,
                 dock_init_strategy=dock.DockStrategyHomeButton,
                 **kwargs):

        self.__display = display_class()
        self.__hu_pm = headunit_pm_class(display=self.__display)
        self.__sc_pm = pm_signals_class()
        self._veh_headunit_pm = veh_pm_class(
            hu_pm=self.__hu_pm, sc_pm=self.__sc_pm)
        if self._veh_headunit_pm.headunit_pm.display != self.__display:
            raise ValueError(
                f"The display of power_manager is not the instance of {self.__class__.__name__}!")
        self.__avm360page = avm360pager_class()
        self.__dock_context = dock_context_class(
            display=self.__display, strategy=dock_init_strategy, avm360page=self.__avm360page)
        if self.__dock_context.display != self.__display:
            raise ValueError(
                f"The display of dock_context is not the instance of {self.__class__.__name__}!")

        super().__init__(
            children=[self.__display, self._veh_headunit_pm.signal_cluster], **kwargs)


