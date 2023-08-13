import ipywidgets as widgets
from IPython.core.display import display

from css import css
from utils.loggers import Logger, OutputWidgetHandler

import logging
logging_handler = OutputWidgetHandler()
_logger = Logger(logger_name=__file__, 
                 log_handler=logging_handler, 
                 logging_level=logging.DEBUG)


class DisplayPanel(widgets.HBox):

    def __init__(self, 
                 width="50%",
                 height="200px",
                 **kwargs):
        
        self.layout = widgets.Layout(
            width=width,
            height=height,
            border="solid",
            justify_content="center",
            align_items="center",
        )

        self.__background = css.BACKGROUND_scree_off
        self.add_class(self.__background)

        self.__forground = widgets.Output(
            layout=widgets.Layout(
                justify_content="center", 
                align_items="center"
                )
        )

        super(DisplayPanel, self).__init__(children=[self.__forground], **kwargs)

    def power_off(self):
        self.__forground.clear_output()
        self.background = css.BACKGROUND_scree_off

    @property
    def forground(self):
        return self.__forground
    
    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, setting: str):

        _logger.debug(f"Setting background to {setting}.")
        self.remove_class(self.__background)
        self.__background = setting
        self.add_class(self.__background)