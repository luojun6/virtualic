import ipywidgets as widgets

from signals.enum_signals import EnhancedUISignalEnum
import signals.saic_signals as signals


class SignalCluster(widgets.VBox):

    def __init__(self, title: str, signal_box: widgets.Box, **kwargs):
        self.__label = widgets.HTML(
            f"<h2 style='font-weight:bold'>{title}</h2>")

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
                 vehicle_door_lock_sts_class=signals.VehLckngSts):
        self.__restart_button = widgets.Button(
            description="RESTART", layout=widgets.Layout(width="auto", justify_content="flex-start"), button_style="danger")
        self.__vehicle_power_mode = EnhancedUISignalEnum(
            vehicle_power_mode_class)
        self.__vehicle_door_lock_sts = EnhancedUISignalEnum(
            vehicle_door_lock_sts_class)

        signal_box = widgets.HBox(
            [self.__restart_button, self.__vehicle_power_mode, self.__vehicle_door_lock_sts])

        super().__init__(
            title="Vehicle Powermanagement Signals Cluster",
            signal_box=signal_box)

    @property
    def restart_button(self):
        return self.__restart_button

    @property
    def vehicle_power_mode(self):
        return self.__vehicle_power_mode

    @property
    def vehicle_door_lock_sts(self):
        return self.__vehicle_door_lock_sts
