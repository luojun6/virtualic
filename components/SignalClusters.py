import ipywidgets as widgets

from signals.enum_signals import EnhancedUISignalEnum
import signals.saic_signals as signals


_SUB_BOX_border = "solid 2px"
_SUB_BOX_margin = "6px"
_SUB_BOX_padding = "6px"
_SUB_BOX_justify_content = "space-around"

class SignalCluster(widgets.VBox):
    
    SUB_BOX_LAYOUT = widgets.Layout(
            border=_SUB_BOX_border, 
            padding=_SUB_BOX_padding, 
            margin=_SUB_BOX_margin,
            justify_content=_SUB_BOX_justify_content)

    def __init__(self, title: str, signal_box: widgets.Box, **kwargs):
        self.__label = widgets.HTML(
            f"<h3 style='font-weight:bold'>{title}</h3>")

        self.__signal_box = signal_box
        self.layout = widgets.Layout(
            border="solid",
            # display="flex",
            # align_items="stretch",
            # flex_flow="wrap",
            justify_content="space-around",
            align_items="center",
        )

        super().__init__(
            children=[self.__label, self.__signal_box], **kwargs)
        

    # @property
    # def signal_box(self):
    #     return self.__signal_box


class SignalClusterPM(SignalCluster):
    
    def __init__(self,
                 vehicle_power_mode_class=signals.SysPwrMd,
                 vehicle_door_lock_sts_class=signals.VehLckngSts,
                #  vehicle_speed_class=signals.VehSpdAvgDrvn,
                #  vehicle_driver_mode_class=signals.VehDrvngMd
                 ):
        self.__restart_button = widgets.Button(
            description="RESTART", layout=widgets.Layout(width="auto", justify_content="flex-start"), button_style="danger")
        self.__vehicle_power_mode = EnhancedUISignalEnum(
            vehicle_power_mode_class)
        self.__vehicle_door_lock_sts = EnhancedUISignalEnum(
            vehicle_door_lock_sts_class)
        # self.__vehicle_speed = vehicle_speed_class()
        # self.__vehicle_driver_mode = EnhancedUISignalEnum(vehicle_driver_mode_class)

        first_row = widgets.HBox(
            [self.__restart_button, self.__vehicle_power_mode, self.__vehicle_door_lock_sts], 
            layout=self.SUB_BOX_LAYOUT)

        # second_row = widgets.HBox(
        #     [self.__vehicle_speed, self.__vehicle_driver_mode],
        #     layout=self.SUB_BOX_LAYOUT
        # )
        
        super().__init__(
            title="Vehicle Powermanagement Signals Cluster",
            signal_box=widgets.VBox([
                first_row
            ]))

    # @property
    # def vehicle_driver_mode(self):
    #     return self.__vehicle_driver_mode
    
    # @property
    # def vehicle_speed(self):
    #     return self.__vehicle_speed 
    
    @property
    def restart_button(self):
        return self.__restart_button

    @property
    def vehicle_power_mode(self):
        return self.__vehicle_power_mode

    @property
    def vehicle_door_lock_sts(self):
        return self.__vehicle_door_lock_sts
