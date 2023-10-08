from common.UISignal import UISignalIntSlider


class SpeedSlider(UISignalIntSlider):
    MIN_SPEED = 0
    MAX_SPEED = 320
    DEFAULT_STEP = 1

    def __init__(self):
        super().__init__(
            signal_name=self.__class__.__name__,
            default_value=self.MIN_SPEED,
            step=self.DEFAULT_STEP,
            min=self.MIN_SPEED,
            max=self.MAX_SPEED,
            orientation="horizontal",
            disabled=False,
            checkbox_description=self.__class__.__name__ + "V"
        )


class SteeringWheelAngle(UISignalIntSlider):
    MIN_ANGLE = -720
    MAX_ANGLE = 720
    DEFAULT_STEP = 1
    
    def __init__(self):
        super().__init__(
            signal_name=self.__class__.__name__,
            default_value=0,
            step=self.DEFAULT_STEP,
            min=self.MIN_ANGLE,
            max=self.MAX_ANGLE,
            orientation="horizontal",
            disabled=False,
            checkbox_description=self.__class__.__name__ + "V"
        )