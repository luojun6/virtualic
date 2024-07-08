import ipywidgets as widgets
from components.PMIC import PowerControlBox
from components.HeadUnit_Internals import SdCardPluginStatus
from components.UserDB import user_db

_CAMERA_ICON = "camera"

class PowerControlBox_SRV360(widgets.VBox):
    
    POWER_ON = "POWER_ON"
    POWER_OFF = "POWER_OFF"
    
    def __init__(self, title="Virtual Power Module Management - SRV360") -> None:
        # self.__PMIC_status = PowerControlBox.POWER_OFF_STATUS
        self.__lablel = widgets.HTML(
            f"<h5 style='font-weight:bold'>{title}</h5>")
        self.__PMIC = PowerControlBox(description=f"PMIC-{PowerControlBox.POWER_OFF_STATUS}")
        self.__front_cam = PowerControlBox(description="front-cam", icon=_CAMERA_ICON)
        self.__rear_cam = PowerControlBox(description="rear_cam", icon=_CAMERA_ICON)
        self.__left_cam = PowerControlBox(description="left-cam", icon=_CAMERA_ICON, justify_content="flex-start")
        self.__right_cam = PowerControlBox(description="right-cam", icon=_CAMERA_ICON, justify_content="flex-end")
        self.__centrl_box = widgets.HBox(
            layout=widgets.Layout(
                width=PowerControlBox.BOX_WIDTH,
                display="flex",
                flex_flow="row",
                align_items="center",
            ),
            children=[self.__left_cam, self.__PMIC, self.__right_cam]
        )
        
        self.__power_status = self.POWER_OFF
        
        self.layout=widgets.Layout(
            display="flex",
            flex_flow="column",
            align_items="center",
            border='solid',
            height="60%"
        )
        super().__init__(
            children=[
                self.__lablel,
                self.__front_cam,
                self.__centrl_box,
                self.__rear_cam
            ])
        
    def __update_PMIC_description(self):
                self.__PMIC.power_status_button.description = f"PMIC-{self.__PMIC.power_status}"
        
    def power_on(self):
        self.__PMIC.power_on()
        self.__update_PMIC_description()
        self.__front_cam.run()
        self.__rear_cam.run()
        self.__left_cam.run()
        self.__right_cam.run()
        self.__power_status = self.POWER_ON
        
    def power_off(self):
        self.__PMIC.power_off()
        self.__update_PMIC_description()
        self.__front_cam.power_off()
        self.__rear_cam.power_off()
        self.__left_cam.power_off()
        self.__right_cam.power_off()
        self.__power_status = self.POWER_OFF
        
    @property
    def power_status(self):
        return self.__power_status
        
        
class ExtremeEnergySaving_SRV360(widgets.VBox):
    EES_SRV360_ENABLED_KEY = "ExtremeEnergySavingSRV360Enabled"
    APP_CLOSE_SPEED_15KMH = 15
    APP_CLOSE_SPEED_25KMH = 25
    APP_CLOSE_SPEED_35KMH = 35
    POWER_CLOSE_SPEED_15KMH = 50
    POWER_CLOSE_SPEED_25KMH = 60
    POWER_CLOSE_SPEED_35KMH = 70
    POWER_ON_SPEED_OFFSET = 4
    
    POWER_CLOSE_MAP = {
        APP_CLOSE_SPEED_15KMH: POWER_CLOSE_SPEED_15KMH,
        APP_CLOSE_SPEED_25KMH: POWER_CLOSE_SPEED_25KMH,
        APP_CLOSE_SPEED_35KMH: POWER_CLOSE_SPEED_35KMH
    }
    
    def __init__(self, 
                 pmic: PowerControlBox_SRV360,
                 sd_card_plugin: SdCardPluginStatus,
                 title="Extreme Energy Saving Setting - SRV360", 
                 close_speed=POWER_CLOSE_SPEED_15KMH, 
                 open_speed=APP_CLOSE_SPEED_15KMH):
        
        self.__pmic = pmic
        self.__sd_card_plugin = sd_card_plugin
        
        self.__lablel = widgets.HTML(
            f"<h5 style='font-weight:bold'>{title}</h5>")
        __applied_checkbox = user_db.get_user_setting(self.EES_SRV360_ENABLED_KEY)
        self.__applied_checkbox = widgets.Checkbox(
            value=__applied_checkbox,
            description="Applied?",
            tooltip = "Applied Extreme Energy Saving for SRV360?",
            button_style = "info",
        )
        self.__close_speed = widgets.IntText(
            value=close_speed,
            description = "close_speed",
            disabled=True
            )
        
        self.__open_speed = widgets.IntText(
            value=open_speed,
            description = "open_speed",
            disabled=True
        )
        
        self.layout=widgets.Layout(
            display="flex",
            flex_flow="column",
            align_items="center",
            border='solid',
            height="40%"
        )
        super().__init__(
            children=[
                self.__lablel,
                # self.__applied_checkbox,
                self.__close_speed,
                self.__open_speed
            ]
        )
        
        self.__applied_checkbox.observe(self.__on_change_applied_checkbox, "value")
        
    def __on_change_applied_checkbox(self, change):
        new_value = change["new"]
        user_db.save_userdb(key=self.EES_SRV360_ENABLED_KEY, value=new_value)
        
    def on_change_speed_callback(self, current_speed):
        
        if self.__sd_card_plugin.value == self.__sd_card_plugin.SD_CARD_PLUG_IN:
            return 
        
        if current_speed > int(self.__close_speed.value):
            self.__pmic.power_off()
            
        elif current_speed < int(self.__open_speed.value + self.POWER_ON_SPEED_OFFSET):
            self.__pmic.power_on()
        
    @property
    def applied_checkbox(self):
        return self.__applied_checkbox
        
    @property
    def close_speed(self):
        return self.__close_speed
    
    @close_speed.setter
    def close_speed(self, value):
        #TODO: validation for input value
        self.__close_speed = value
    
    @property
    def open_speed(self):
        return self.__open_speed
    
    @open_speed.setter
    def open_speed(self, value):
        #TODO: validation for input value
        self.__open_speed = value