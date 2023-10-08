import ipywidgets as widgets
from components.PMIC import PowerControlBox

_CAMERA_ICON = "camera"

class PowerControlBox_AVM360(widgets.VBox):
    
    def __init__(self) -> None:
        # self.__PMIC_status = PowerControlBox.POWER_OFF_STATUS
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
                align_items="center"
            ),
            children=[self.__left_cam, self.__PMIC, self.__right_cam]
        )
        
        self.layout=widgets.Layout(
            display="flex",
            flex_flow="column",
            align_items="center"
        )
        super().__init__(
            children=[
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
        
    def power_off(self):
        self.__PMIC.power_off()
        self.__update_PMIC_description()
        self.__front_cam.power_off()
        self.__rear_cam.power_off()
        self.__left_cam.power_off()
        self.__right_cam.power_off()