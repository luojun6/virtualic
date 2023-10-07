import components.ForgroundPages as pages
import ipywidgets as widgets

from IPython.core.display import display
from abc import ABC, abstractmethod

from css import css

from components.DisplayPanel import DisplayPanel
from components.UserDB import user_db

from utils.threading_timer import debounce


from utils.loggers import Logger, logging_handler
import logging


_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)


class PowerState(ABC):
    state_duration = 0

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def execute(self) -> None:
        _logger.debug(f"Executing {self.__class__.__name__}.")
        for child in self.context.display.children:
            child.clear_output()

    @debounce(state_duration)
    def transition_to(self, state):
        _logger.debug(f"Transitting to {state.__class__.__name__}.")

        self.context.transition_to(state)
        # self.context.current_power_state = state.__class__.__name__

    # def __str__(self) -> str:
    #     return self.name


class PowerStateOFF(PowerState):

    def execute(self):
        super().execute()
        self.context.display.power_off()
        self.context.display.layout.justify_content = "center"


class PowerStateStartUp(PowerState):
    state_duration = 0.2

    def __init__(self, power_up_state: PowerState):
        self.__power_up_state = power_up_state

    def execute(self):
        super().execute()
        html = widgets.HTML(
            "<h3 style='font-weight:bold'>System is starting up....</h3>")
        html.add_class(css.FONT_color_night)
        # html.value = "<h3 style='font-weight:bold'>Dislaying start-up animation....</h3>"

        with self.context.display.forground:
            display(html)

        self.transition_to_power_up()

    @debounce(state_duration)
    def transition_to_power_up(self):
        self.transition_to(self.__power_up_state)
        # self.context.display.forground.clear_output()


class PowerStatePowerUp(PowerState):
    state_duration = 3

    def __init__(self, running_state: PowerState) -> None:
        self.__running_state = running_state

    def execute(self) -> None:
        super().execute()

        html = widgets.HTML(
            "<h3 style='font-weight:bold'>Dislaying power-up animation....</h3>")

        with self.context.display.forground:
            display(html)

        theme_value = css.BACKGROUND_theme_night

        if self.context.user_db:
            theme_key = self.context.user_db.theme_day_night_setting
            db_theme_value = self.context.user_db.get_user_setting(theme_key)
            _logger.debug(
                f"Fetching {theme_key} : {db_theme_value} from user_db.")
            if db_theme_value:
                theme_value = db_theme_value

        self.context.display.background = theme_value

        html.add_class(theme_value.replace("theme", "font_color"))

        self.transition_to_running()

    @debounce(state_duration)
    def transition_to_running(self):
        self.context.display.power_on()
        self.transition_to(self.__running_state)
        # self.context.display.forground.clear_output()


class PowerStateRunning(PowerState):

    def execute(self) -> None:
        super().execute()
        
        self.context.display.layout.justify_content = "flex-start"
        
        with self.context.display.dock:
            display(self.context.display.dock_buttons)

        with self.context.display.forground:
            display(pages.HOME_PAGE_0)


class PowerManagementContext:

    _state = None

    def __init__(self, state) -> None:
        self.transition_to(state)

        self.__current_power_state = state.__class__.__name__

    def transition_to(self, state) -> None:
        self._state = state
        self._state.context = self
        state.execute()

    @property
    def current_power_state(self):
        return self.__current_power_state

    @current_power_state.setter
    def current_power_state(self, state: str):
        self.__current_power_state = state


class PowerManagementDisplay(PowerManagementContext):

    def __init__(self,
                 display: DisplayPanel,
                 user_db=user_db,
                 power_off_state=PowerStateOFF,
                 start_up_state=PowerStateStartUp,
                 power_up_state=PowerStatePowerUp,
                 running_state=PowerStateRunning
                 ):
        self.__user_db = user_db
        self.__running_state = running_state()
        self.__power_up_state = power_up_state(self.__running_state)
        self.__start_up_state = start_up_state(self.__power_up_state)
        self.__power_off_state = power_off_state()
        self.__display = display

        # self.transition_to(self.__power_off_state)

        super().__init__(state=self.__power_off_state)

    def transition_to(self, state) -> None:
        super().transition_to(state)
        self.current_power_state = state.__class__.__name__

    @property
    def user_db(self):
        return self.__user_db

    @property
    def display(self):
        return self.__display

    def power_off(self):
        if self.current_power_state != self.__power_off_state.__class__.__name__:
            self.transition_to(self.__power_off_state)

    def start_up(self):
        if self.current_power_state == self.__power_off_state.__class__.__name__:
            self.transition_to(self.__start_up_state)
