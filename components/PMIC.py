import ipywidgets as widgets




_WIDTH = "120px"
_HEIGHT = "40px"
_PLUG_ICON = "plug"

class PowerControlBox(widgets.HBox):
    
    BOX_WIDTH = "360px"
    
    POWER_OFF_STATUS = "OFF"
    POWER_ON_STATUS = "ON"
    POWER_RUNNING_STATUS = "RUNNING"
    
    POWER_STATUS_STYLE_MAP = {
        POWER_OFF_STATUS: "",
        POWER_ON_STATUS: "danger",
        POWER_RUNNING_STATUS: "warning"
    }
    
    def __init__(self, 
                 description: str, 
                 justify_content="center", 
                 icon=_PLUG_ICON,
                 box_width=BOX_WIDTH,
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
        
        self.__power_status = self.POWER_OFF_STATUS   # Initial power status
        
        super().__init__(children=[self.__button], **kwargs)
        
    @property
    def power_status_button(self):
        return self.__button
    
    @property
    def power_status(self):
        return self.__power_status
    
    def __update_button_style(self):
        self.__button.button_style = self.POWER_STATUS_STYLE_MAP[self.power_status]
    
    def power_on(self):
        self.__power_status = self.POWER_ON_STATUS
        self.__update_button_style()
        
    def power_off(self):
        self.__power_status = self.POWER_OFF_STATUS
        self.__update_button_style()
        
    def run(self):
        self.__power_status = self.POWER_RUNNING_STATUS
        self.__update_button_style()