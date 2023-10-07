import ipywidgets as widgets



_BOX_WIDTH = "360px"
_WIDTH = "120px"
_HEIGHT = "40px"
_PLUG_ICON = "plug"

class PowerControlBox(widgets.HBox):
    
    POWER_ON_STYLE = "danger"
    POWER_OFF_STYLE = ""
    POWER_RUN_STYLE = "warning"
    
    def __init__(self, 
                 description: str, 
                 justify_content="center", 
                 icon=_PLUG_ICON,
                 power_off_button_style=POWER_OFF_STYLE,
                 power_on_button_style=POWER_ON_STYLE,
                 run_status_button_style=POWER_RUN_STYLE,
                 box_width=_BOX_WIDTH,
                 width=_WIDTH,
                 height=_HEIGHT,
                 **kwargs):
        self.layout = widgets.Layout(
            width=box_width,
            align_items="center",
            justify_content=justify_content
        )
        
        self.__button = widgets.Button(
            description=description,
            button_style="",
            icon=icon,
            layout=widgets.Layout(
                width=width,
                height=height
            )
        )
        
        self.__power_off_button_style = power_off_button_style
        self.__power_on_button_style = power_on_button_style
        self.__run_status_button_style = run_status_button_style
        
        super().__init__(children=[self.__button], **kwargs)
        
    @property
    def power_status_button(self):
        return self.__button
    
    def power_on(self):
        self.__button.button_style = self.__power_on_button_style
        
    def power_off(self):
        self.__button.button_style = self.__power_off_button_style
        
    def run(self):
        self.__button.button_style = self.__run_status_button_style