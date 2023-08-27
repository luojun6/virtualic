from threading import Event

from components.SignalClusters import SignalClusterPM
from common.AbstractCommand import Command
from rules.HeadUnitPM import PowerManagementDisplay as HeadUnitPM

from utils.loggers import Logger, logging_handler
import logging


_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)


class VehicleKeyOnCommand(Command):

    def execute(self):
        self.receiver.start_up()


class VehiclePowerOffCommand(Command):

    def execute(self):
        self.receiver.power_off()


class VehicleHeadUnitPM_SAIC():

    def __init__(self, hu_pm: HeadUnitPM, sc_pm: SignalClusterPM):
        self.__hu_pm = hu_pm
        self.__sc_pm = sc_pm
        self.__key_on_cmd = VehicleKeyOnCommand(self.__hu_pm)
        self.__power_off_cmd = VehiclePowerOffCommand(self.__hu_pm)

        self.__key_off_event = Event()
        self.__power_off_event = Event()
        self.__key_off_event.set()
        self.__power_off_event.set()

        self.__sc_pm.restart_button.on_click(self.__on_click_restart_button)
        self.__sc_pm.vehicle_power_mode.set_on_change_callback(
            self.__on_change_vehicle_power_mode)
        self.__sc_pm.vehicle_door_lock_sts.set_on_change_callback(
            self.__on_change_vehicle_door_lock_sts
        )

    @property
    def headunit_pm(self):
        return self.__hu_pm

    @property
    def signal_cluster(self):
        return self.__sc_pm

    def __on_click_restart_button(self, button):
        self.__hu_pm.power_off()
        self.__hu_pm.start_up()

    def __on_change_vehicle_power_mode(self, change):
        new_value = change["new"]
        signal = self.__sc_pm.vehicle_power_mode.signal
        _logger.debug(
            f"Received vehicle power mode change with signal_name: {signal.__name__}, value: {new_value}.")

        if new_value == signal.RUN.value:
            if self.__power_off_event.is_set():
                self.__key_on_cmd.execute()
                self.__key_off_event.clear()
                self.__power_off_event.clear()

            else:
                _logger.error(
                    f"Do not execute {self.__key_on_cmd.__class__.__name__} while power_off_event is {self.__power_off_event.is_set()}.")

        elif new_value == signal.OFF.value:
            # self.__key_off_cmd.execute()
            self.__key_off_event.set()

    def __on_change_vehicle_door_lock_sts(self, change):
        new_value = change["new"]
        signal = self.__sc_pm.vehicle_door_lock_sts.signal

        _logger.debug(
            f"Received vehicle door lock status change with signal_name: {signal.__name__}, value: {new_value}.")

        if new_value == signal.Super_Locked.value:
            if self.__key_off_event.is_set():
                self.__power_off_cmd.execute()
                self.__power_off_event.set()
