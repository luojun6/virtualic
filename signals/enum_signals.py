from enum import Enum
import ipywidgets as widgets

from common.UISignal import UISignalEnum


class EnumSignal(Enum):
    @classmethod
    # @property
    def get_option_tuples(cls):
        if len(cls) == 0:
            raise ValueError(f"{cls.__name__} is an empty signal!!!")

        names = [e.name for e in list(cls)]
        values = [e.value for e in list(cls)]

        return list(zip(names, values))

    def __str__(self) -> str:
        return self.name


class EnhancedUISignalEnum(UISignalEnum):
    def __init__(
        self,
        signal: EnumSignal,
        initial_value=0,
        select_widget_type=widgets.Dropdown,
        disabled=False,
    ):
        self.__signal = signal

        super().__init__(
            signal_name=self.__signal.__name__.replace("EnumSignal", ""),
            initial_value=initial_value,
            select_widget_type=select_widget_type,
            disabled=disabled,
            tuples_option=self.__signal.get_option_tuples(),
        )

    @property
    def signal(self):
        return self.__signal
