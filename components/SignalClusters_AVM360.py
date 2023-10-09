import ipywidgets as widgets

from signals.enum_signals import EnhancedUISignalEnum
import signals.saic_signals as signals

from components.SignalClusters import SignalCluster

class SignalClusterAVM360(SignalCluster):
    def __init__(self,
                 gear_sts_class=signals.TrShftLvrPos,
                 turn_light_sw_class=signals.DircnIndLampSwSts,
                 left_turnning_light_sts_class=signals.LDircnIO,
                 right_turnning_light_sts_class=signals.RDircnIO,
                 steering_wheel_angle_class=signals.StrgWhlAng,
                 vehicle_speed_class=signals.VehSpdAvgDrvn,
                 vehicle_driver_mode_class=signals.VehDrvngMd
                 ):
        
        self.__gear_sts=EnhancedUISignalEnum(gear_sts_class, checkbox_description_plus_V=True)
        self.__turn_light_sw=EnhancedUISignalEnum(turn_light_sw_class)
        self.__left_turnning_light_sts=EnhancedUISignalEnum(left_turnning_light_sts_class)
        self.__right_turnning_light_sts=EnhancedUISignalEnum(right_turnning_light_sts_class)
        self.__steering_wheel_angle=steering_wheel_angle_class()
        self.__vehicle_speed = vehicle_speed_class()
        self.__vehicle_driver_mode = EnhancedUISignalEnum(vehicle_driver_mode_class)
        
        first_row = widgets.HBox(
            [self.__gear_sts, self.__vehicle_speed],
            layout=self.SUB_BOX_LAYOUT
        )

        second_row = widgets.HBox(
            [self.__turn_light_sw, self.__vehicle_driver_mode]
        )
        
        third_row = widgets.HBox(
            [self.__left_turnning_light_sts, self.__right_turnning_light_sts],
            layout=self.SUB_BOX_LAYOUT
        )
        
        super().__init__(
            title="AVM360 Signals Cluster", 
            signal_box=widgets.VBox([
                first_row, third_row
            ]))
        
    @property
    def gear_sts(self):
        return self.__gear_sts
    
    @property
    def turn_light_sw(self):
        return self.__turn_light_sw
    
    @property
    def left_turnning_light_sts(self):
        return self.__left_turnning_light_sts
    
    @property
    def right_turnning_light_sts(self):
        return self.__right_turnning_light_sts
    
    @property
    def steering_wheel_angle(self):
        return self.__steering_wheel_angle

    @property
    def vehicle_driver_mode(self):
        return self.__vehicle_driver_mode
    
    @property
    def vehicle_speed(self):
        return self.__vehicle_speed 



