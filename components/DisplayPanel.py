import ipywidgets as widgets
# from IPython.core.display import display

from css import css
from components.DockButtons import DockButtons
from utils.loggers import Logger, logging_handler
import logging

_logger = Logger(logger_name=__file__,
                 log_handler=logging_handler,
                 logging_level=logging.DEBUG)


class DisplayPanel(widgets.HBox):

    def __init__(self,
                 width="50%",
                 height="300px",
                 dock_buttons_class=DockButtons,
                 **kwargs):

        self.layout = widgets.Layout(
            width=width,
            height=height,
            border="solid",
            justify_content="center",
            align_items="center",
        )
        self.__dock_buttons = dock_buttons_class()
        self.__background = css.BACKGROUND_scree_off
        self.add_class(self.__background)

        self.__foreground = widgets.Output(
            layout=widgets.Layout(
                # width="90%",
                # height="auto",
                justify_content="space-around",
                align_items="center"
            )
        )

        self.__dock = widgets.Output(
            layout=widgets.Layout(
                width="58px"
            )
        )
        

        super(DisplayPanel, self).__init__(
            # children=[self.__dock, self.__foreground], 
            children=[self.__foreground], 
            **kwargs)

    def power_off(self):
        self.__foreground.clear_output()
        self.__dock.clear_output()
        self.background = css.BACKGROUND_scree_off
        self.children = [self.__foreground]
        
    def power_on(self):
        self.children = [self.__dock, self.__foreground]

    @property
    def dock(self):
        return self.__dock

    @property
    def dock_buttons(self):
        return self.__dock_buttons

    @property
    def foreground(self):
        return self.__foreground

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, setting: str):

        _logger.debug(f"Setting background to {setting}.")
        self.remove_class(self.__background)
        self.__background = setting
        self.add_class(self.__background)
        
    def clear_all_output(self):
        self.__foreground.clear_output()
        self.__dock.clear_output()
