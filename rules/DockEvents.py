from abc import ABC, abstractmethod
from IPython.core.display import display
from components.VirtualSystem import VituralSystemContext
import components.ForegroundPages as pages
from rules.AbstractStrategies import AbstractOnClickStrategy
from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)

class DockContext(VituralSystemContext):
    
    def __init__(self):
        super().__init__()
        
        self.__init_strategies()

    # Step 1: Configure Concrete Strategy 
    def __init_strategies(self):
        self.__home_button_strategy = OnClickHomeButton()
        self.__srv360_button_strategy = OnClickSrv360Button()
    
    # Step 2: Define callback function        
    def __on_click_home_button(self, button):
        self.__home_button_strategy.execute(context=self, button=button)
        
    def __on_click_srv360_button(self, button):
        self.__srv360_button_strategy.execute(context=self, button=button)
    
    # Step 3: Register callback functions
    # Executed in parent constructor
    def register_callbacks(self):
        self.system.display.dock_buttons.home_button.on_click(self.__on_click_home_button)
        self.system.display.dock_buttons.srv360_button.on_click(self.__on_click_srv360_button)
        
    def clear_display_outputs(self):
        self.system.display.clear_all_output()    
    
    def enter_home_page(self):
        self.clear_display_outputs()
        
        with self.system.display.foreground:
            display(pages.HOME_PAGE_0)

        with self.system.display.dock:
            display(self.system.display.dock_buttons)
    
class OnClickHomeButton(AbstractOnClickStrategy):
    
    def execute(self, context, button):
        context.enter_home_page()
        # context.clear_display_outputs()
        
        # with context.system.display.foreground:
        #     display(pages.HOME_PAGE_0)

        # with context.system.display.dock:
        #     display(context.system.display.dock_buttons)
    
class OnClickSrv360Button(AbstractOnClickStrategy):
    
    def execute(self, context, button):
        context.system.srv360context.dock_enter()


class OldDockContext(VituralSystemContext):

    def __init__(self):
        super(OldDockContext, self).__init__()
        self.__strategy = DockStrategyHomeButton()

        
    def register_callbacks(self):
        self.system.display.dock_buttons.home_button.on_click(
            self.__on_click_home_button)
        self.system.display.dock_buttons.srv360_button.on_click(
            self.__on_click_srv360_button)
        
       
        

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, new_strategy) -> None:
        self.__strategy = new_strategy
        

    def process_button_pressed_event(self) -> None:
        _logger.debug(
            f"Processing button_pressed_event with strategy: {self.__strategy.__class__.__name__}.")
        self.system.display.clear_all_output()
        self.__strategy.process_button_pressed_event(self)
        
    def enter_home_page(self):
        self.__strategy = DockStrategyHomeButton()
        self.process_button_pressed_event()
        
        
    def __on_click_home_button(self, button):
        self.enter_home_page()

    def __on_click_srv360_button(self, button):
        self.__strategy = DockStrategySRV360button()
        self.process_button_pressed_event()


class _DockStrategy(ABC):

    @abstractmethod
    def process_button_pressed_event(self, context: OldDockContext):
        pass


class DockStrategyHomeButton(_DockStrategy):

    def process_button_pressed_event(self, context):
        with context.system.display.foreground:
            display(pages.HOME_PAGE_0)

        with context.system.display.dock:
            display(context.system.display.dock_buttons)
    


class DockStrategySRV360button(_DockStrategy):

    def process_button_pressed_event(self, context):
        context.system.srv360context.dock_entered()

        
            