import threading
from IPython.core.display import display
from common.ipywidgetsUtilities import get_output_model_id
from components.AVM360Page import AVM360Page
from components.VirtualSystem import VituralSystemContext
from components.SignalClusters_AVM360 import SignalClusterAVM360
from components.PMIC_AVM360 import PowerControlBox_AVM360
from rules.AbstractStrategies import AbstractOnChangeStrategy, AbstractStrategy
import rules.FakedBCM as BCM

from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)
    
    
class AVM360Context(VituralSystemContext):
    
    # def __init__(self, headunit: VirtualHeadUnit):
    def __init__(self):
        # self.__display = self.system.display
        self.__avm360page = AVM360Page()
        
        self.__signal_cluster = SignalClusterAVM360()
        self.__pmic = PowerControlBox_AVM360()
        self.__dock_entered = threading.Event()
        self.__turn_light_entered = threading.Event()
        
        super().__init__()
        
        self.__init_strategies()
        
        
    # Step 1: Configure Concrete Strategy 
    def __init_strategies(self):
        self.on_speed_for_enable()
        self.__on_change_gear_sts_strategy = OnChangeGearStatus()
        self.__on_change_speed_strategy = OnChangeSpeed()
        self.__dock_enter_strategy = DockEnterStrategy()
        self.__on_change_turn_light_switch_strategy = OnChangeTurnLightSwitch()
        self.__on_change_left_turn_light_status_strategy = OnChnageLeftTurnLightStatus()
        self.__on_change_right_turn_light_status_strategy = OnChnageRightTurnLightStatus()
    
    # Step 2: Define callback function    
    def __on_change_gear_sts(self, change):
        self.__on_change_gear_sts_strategy.execute(context=self, change=change)
        
    def __on_change_speed(self, change):
        self.__on_change_speed_strategy.execute(context=self, change=change)
        
    def __on_change_turn_light_switch(self, change):
        self.__on_change_turn_light_switch_strategy.execute(context=self, change=change)
        
    def __on_change_left_turn_light_status(self, change):
        self.__on_change_left_turn_light_status_strategy.execute(context=self, change=change)
        
    def __on_change_right_turn_light_status(self, change):
        self.__on_change_right_turn_light_status_strategy.execute(context=self, change=change)
        
    # Step 3: Register callback functions
    # Executed in parent constructor
    def register_callbacks(self):
        self.__avm360page.home_button.on_click(self.__exit_avm360page_button_callback)
        self.__signal_cluster.gear_sts.set_on_change_callback(self.__on_change_gear_sts)
        self.__signal_cluster.vehicle_speed.set_on_change_callback(self.__on_change_speed)
        self.__signal_cluster.turn_light_sw.set_on_change_callback(self.__on_change_turn_light_switch)
        self.__signal_cluster.left_turnning_light_sts.set_on_change_callback(self.__on_change_left_turn_light_status)
        self.__signal_cluster.right_turnning_light_sts.set_on_change_callback(self.__on_change_right_turn_light_status)
        
    def on_speed_for_enable(self):
        current_speed = self.get_vehicle_speed()
        closed_speed_setting = self.get_closespeed_setting_value()
        if current_speed < closed_speed_setting:
            self.enable()
        else:
            self.disable()
            
        
    def __exit_avm360page_button_callback(self, button):
        self.exit_avm360page()
        
    def exit_avm360page(self):
        self.avm360page.exit_setting_page()
        self.system.dock_context.enter_home_page()
        self.__turn_light_entered.clear()
        self.__dock_entered.clear()
        self.avm360page.clear_setting()
        
    def power_on(self):
        self.__pmic.power_on()
        self.enable()
        
    def power_off(self):
        self.__pmic.power_off()
        self.disable()    
        
    
    
    @property
    def pmic(self):
        return self.__pmic
        
    @property
    def signal_cluster(self):
        return self.__signal_cluster
        
    @property
    def avm360page(self):
        return self.__avm360page    
    
    def dock_enter(self):
        self.__dock_enter_strategy.execute(context=self)
        
    @property
    def dock_entered_event(self):
        return self.__dock_entered
    
    @property
    def turn_light_entered_event(self):
        return self.__turn_light_entered
        
    def is_avm360page(self):
        return get_output_model_id(self.system.display.foreground) == self.__avm360page.model_id
    
    def enter_avm360page(self):
        _logger.debug("Entered avm360page.")
        if not self.is_avm360page():
        
            with self.system.display.foreground:
                display(self.__avm360page)
                
        else:
            _logger.error("Already in avm360page!")
            
    def get_closespeed_setting_value(self):
        return int(self.avm360page.avm360_setting_page.user_setting_closespeed_value.replace("km/h", ""))

    def get_vehicle_speed(self):
        return int(self.signal_cluster.vehicle_speed.value)
    
    
class OnChnageRightTurnLightStatus(AbstractOnChangeStrategy):
    
    def execute(self, context, change):
        if not context.is_enabled:
            return
        
        new_value = change["new"]
        signal = context.signal_cluster.right_turnning_light_sts.signal
        
        if new_value == signal.OFF.value:
            if context.is_avm360page():
                context.exit_avm360page()
                context.turn_light_entered_event.clear()
    
    
class OnChnageLeftTurnLightStatus(AbstractOnChangeStrategy):
    
    def execute(self, context, change):
        if not context.is_enabled:
            return
        
        new_value = change["new"]
        signal = context.signal_cluster.left_turnning_light_sts.signal
        
        if new_value == signal.OFF.value:
            if context.is_avm360page():
                context.exit_avm360page()
                context.turn_light_entered_event.clear()
                

class OnChangeTurnLightSwitch(AbstractOnChangeStrategy):
    
    def execute(self, context, change):
        
        BCM.TurnLight().execute(context=context)
        
        if not context.is_enabled:
            return

        new_value = change["new"]
        signal = context.signal_cluster.turn_light_sw.signal
        
        if (new_value == signal.Left_On.value) or (new_value == signal.Right_On.value):
            if not context.is_avm360page():
                context.system.display.clear_all_output()
                context.enter_avm360page()
                context.turn_light_entered_event.set()
                
                
                
        
             
                
class OnChangeGearStatus(AbstractOnChangeStrategy):
    
    def execute(self, context, change):
        if not context.is_enabled:
            return
        
        new_value = change["new"]
        signal = context.signal_cluster.gear_sts.signal
        
        if new_value == signal.ReverseRange.value:
            if not context.is_avm360page():
                context.system.display.clear_all_output()
                context.enter_avm360page()
            
        else:
            if context.is_avm360page():
                context.exit_avm360page()


class OnChangeSpeed(AbstractOnChangeStrategy):
    
    def execute(self, context, change):

        context.on_speed_for_enable()
        
        if not context.is_enabled:
            if context.is_avm360page():
                context.exit_avm360page()


class DockEnterStrategy(AbstractStrategy):
    
    def execute(self, context):
       
        if context.is_enabled:
            context.system.display.clear_all_output() 

            context.dock_entered_event.set()
            context.enter_avm360page()
            
        else:
            _logger.warn("Current vehicle speed is not allowed to enter avm360page.")
            