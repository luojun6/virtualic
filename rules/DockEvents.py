from abc import ABC, abstractmethod
from IPython.core.display import display
from components.VirtualSystem import VituralSystemContext
from components.VirtualSystem_HeadUnit import VirtualSystem_HeadUnit
import components.ForgroundPages as pages

from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)





class DockContext(VituralSystemContext):

    def __init__(self):
        # self.__display = self.system.display
        super(DockContext, self).__init__()
        self.__strategy = DockStrategyHomeButton()
        # self.__avm360context = self.system.avm360context


        # self.__avm360context.avm360page.home_button.on_click(self.__on_click_home_button)

    # @property
    # def display(self):
    #     return self.__display
    
    # @property
    # def avm360context(self):
    #     return self.__avm360context
    
    def run(self):
        self.__register_buttons_callback()
        # super().start()
        
        
    def __register_buttons_callback(self):
        
        self.system.display.dock_buttons.home_button.on_click(
            self.__on_click_home_button)
        self.system.display.dock_buttons.avm360_button.on_click(
            self.__on_click_avm360_button)
        

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, new_strategy) -> None:
        self.__strategy = new_strategy

    def process_button_pressed_event(self) -> None:
        _logger.debug(
            f"Processing button_pressed_event with strategy: {self.__strategy.__class__.__name__}.")
        # self.__display.dock.clear_output()
        # self.__display.forground.clear_output()
        self.system.display.clear_all_output()
        self.__strategy.process_button_pressed_event(self)
        
    def enter_home_page(self):
        self.__strategy = DockStrategyHomeButton()
        self.process_button_pressed_event()
        
    def __on_click_home_button(self, button):
        self.enter_home_page()

    def __on_click_avm360_button(self, button):
        self.__strategy = DockStrategyAVM360button()
        self.process_button_pressed_event()


class _DockStrategy(ABC):

    @abstractmethod
    def process_button_pressed_event(self, context: DockContext):
        pass


class DockStrategyHomeButton(_DockStrategy):

    def process_button_pressed_event(self, context):
        with context.system.display.forground:
            display(pages.HOME_PAGE_0)

        with context.system.display.dock:
            display(context.display.dock_buttons)
        
        context.system.avm360context.dock_entered.clear()
        context.system.avm360context.on_avm360page.clear()


class DockStrategyAVM360button(_DockStrategy):

    def process_button_pressed_event(self, context):
        with context.system.display.forground:
            display(context.avm360context.avm360page)
        
        context.system.avm360context.dock_entered.set()
        context.system.avm360context.on_avm360page.set()
        
            
        
