from common.UISignal import UISignalIntSlider


class SpeedSlider(UISignalIntSlider):
    MIN_SPEED = 0
    MAX_SPEED = 320
    DEFAULT_STEP = 1

    def __init__(
        self,
        signal_name=__name__,
        default_value=MIN_SPEED,
        min=MIN_SPEED,
        max=MAX_SPEED,
        orientation="horizontal",
        disabled=False,
        checkbox_description=__name__ + "V",
        **kwargs
    ):
        super().__init__(
            default_value,
            min,
            max,
            signal_name,
            orientation,
            disabled,
            checkbox_description,
            **kwargs
        )
