from abc import ABC, abstractmethod
from IPython.core.display import display
from components.AVM360Page import AVM360Page
import components.ForgroundPages as pages
from components.DisplayPanel import DisplayPanel

from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)


class _DockStrategy(ABC):

    @abstractmethod
    def process_button_pressed_event(self, context):
        pass


class DockContext:

    def __init__(self, display: DisplayPanel, strategy: _DockStrategy, avm360page: AVM360Page):
        self.__display = display
        self.__strategy = strategy
        self.__avm360page = avm360page

        self.__display.dock_buttons.home_button.on_click(
            self.__on_click_home_button)
        self.__display.dock_buttons.avm360_button.on_click(
            self.__on_click_avm360_button)

        self.__avm360page.home_button.on_click(self.__on_click_home_button)

    @property
    def display(self) -> DisplayPanel:
        return self.__display

    @property
    def avm360page(self):
        return self.__avm360page

    @property
    def strategy(self) -> _DockStrategy:
        return self.__strategy

    @strategy.setter
    def strategy(self, new_strategy) -> None:
        self.__strategy = new_strategy

    def process_button_pressed_event(self) -> None:
        _logger.debug(
            f"Processing button_pressed_event with strategy: {self.__strategy.__class__.__name__}.")
        self.__display.dock.clear_output()
        self.__display.forground.clear_output()
        self.__strategy.process_button_pressed_event(self)

    def __on_click_home_button(self, button):
        self.__strategy = DockStrategyHomeButton()
        self.process_button_pressed_event()

    def __on_click_avm360_button(self, button):
        self.__strategy = DockStrategyAVM360button()
        self.process_button_pressed_event()


class DockStrategyHomeButton(_DockStrategy):

    def process_button_pressed_event(self, context):
        with context.display.forground:
            display(pages.HOME_PAGE_0)

        with context.display.dock:
            display(context.display.dock_buttons)


class DockStrategyAVM360button(_DockStrategy):

    def process_button_pressed_event(self, context):
        with context.display.forground:
            display(context.avm360page)
