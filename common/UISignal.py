from abc import abstractmethod
import ipywidgets as widgets
from typing import Type, Tuple


class _UISignal(widgets.VBox):
    def __init__(
        self,
        signal_name: str,
        disabled=False,
        checkbox_description="disable",
        **kwargs,
    ):
        self.__label = widgets.HTML(f"<h4 style='font-weight:bold'>{signal_name}</h4>")
        self.__checkbox = widgets.Checkbox(
            value=disabled,
            description=checkbox_description,
        )
        self.__value_widget = self.construct_value_widget()

        super().__init__(
            children=[
                widgets.HBox(
                    [self.__label, self.__checkbox],
                ),
                self.__value_widget,
            ],
            layout=widgets.Layout(align_items="center"),
            **kwargs,
        )

        self.__checkbox.observe(self.__on_change_checkbox, "value")

    # To be overriden
    @abstractmethod
    def construct_value_widget(self):
        pass

    def __on_change_checkbox(self, change):
        self.__value_widget.disabled = change["new"]

    def set_on_change_callback(self, callback):
        self.__value_widget.observe(callback, "value")

    @property
    def label(self):
        return self.__label

    @property
    def value_widget(self):
        return self.__value_widget

    @property
    def value(self):
        return self.__value_widget.value

    @value.setter
    def value(self, new_value):
        self.__value_widget.value = new_value

    @property
    def value_widget(self):
        return self.__value_widget

    @property
    def check_box(self):
        return self.__checkbox


class UISignalIntSlider(_UISignal):
    def __init__(
        self,
        default_value: int,
        min: int,
        max: int,
        step: int,
        signal_name: str,
        orientation="horizontal",
        disabled=False,
        checkbox_description="disable",
        **kwargs,
    ):
        self.__default_value = default_value
        self.__min = min
        self.__max = max
        self.__step = step
        self.__orientation = orientation
        super().__init__(signal_name, disabled, checkbox_description, **kwargs)

    def construct_value_widget(self):
        return widgets.IntSlider(
            value=self.__default_value,
            min=self.__min,
            max=self.__max,
            step=self.__step,
            orientation=self.__orientation,
        )


class UISignalEnum(_UISignal):
    def __init__(
        self,
        tuples_option: Type[Tuple],
        signal_name: str,
        initial_value=0,
        disabled=False,
        checkbox_description="disable",
        **kwargs,
    ):
        self.__tuples_option = tuples_option
        self.__initial_value = initial_value
        self.__default_disable_status = disabled
        super().__init__(signal_name, disabled, checkbox_description, **kwargs)

    def construct_value_widget(self):
        return widgets.Dropdown(
            options=self.__tuples_option,
            value=self.__initial_value,
            disabled=self.__default_disable_status,
        )
