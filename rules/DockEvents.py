from abc import ABC, abstractmethod
from IPython.core.display import display
# from components.VirtualHeadUnit import VirtualHeadUnit
import components.ForgroundPages as pages

from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)





class DockContext:

    # def __init__(self, headunit: VirtualHeadUnit):
    def __init__(self, headunit):
        self.__display = headunit.display
        self.__strategy = DockStrategyHomeButton()
        self.__avm360service = headunit.avm360service

        self.__display.dock_buttons.home_button.on_click(
            self.__on_click_home_button)
        self.__display.dock_buttons.avm360_button.on_click(
            self.__on_click_avm360_button)

        # self.__avm360service.avm360page.home_button.on_click(self.__on_click_home_button)

    @property
    def display(self):
        return self.__display
    
    @property
    def avm360service(self):
        return self.__avm360service

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
        self.__display.clear_all_output()
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
        with context.display.forground:
            display(pages.HOME_PAGE_0)

        with context.display.dock:
            display(context.display.dock_buttons)
        
        context.avm360service.dock_entered.clear()
        context.avm360service.on_avm360page.clear()


class DockStrategyAVM360button(_DockStrategy):

    def process_button_pressed_event(self, context):
        with context.display.forground:
            display(context.avm360service.avm360page)
        
        context.avm360service.dock_entered.set()
        context.avm360service.on_avm360page.set()
        
            
        
