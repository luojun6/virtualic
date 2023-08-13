from typing import Type
import ipywidgets as widgets
from abc import ABC, abstractmethod
from ipywidgets import Button, HBox, ValueWidget


class Context(ValueWidget):
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    _state = None
    """
    A reference to the current state of the Context.
    """

    # def __init__(self, state: State) -> None:
    def __init__(self, state) -> None:
        self.__init_state = state
        self.transition_to(state)

        self.__next_button = Button(
            description="NEXT", button_style="info", icon="arrow-right"
        )
        self.__next_button.on_click(self.__on_click_next_button)

        self.__reset_button = Button(
            description="RESET", button_style="info", icon="power-off"
        )
        self.__reset_button.on_click(self.__on_click_reset_button)
        self.__on_click_reset_button_addtional_callback = None

    # def transition_to(self, state: State):
    def transition_to(self, state):
        """
        The Context allows changing the State object at runtime.
        """

        # print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    The Context delegates part of its behavior to the current State object.
    """

    @property
    def hbox_buttons(self):
        return HBox([self.__reset_button, self.__next_button])

    @property
    def next_button(self):
        return self.__next_button

    @property
    def reset_button(self):
        return self.__reset_button

    def set_on_click_reset_button_additional_callback(self, callback):
        self.__on_click_reset_button_addtional_callback = callback

    def __on_click_next_button(self, btn):
        self._state.handle_next_button_click()

    def __on_click_reset_button(self, btn):
        if self.__on_click_reset_button_addtional_callback:
            self.__on_click_reset_button_addtional_callback()
        self.__init_state.execute()
        self.transition_to(self.__init_state)


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def handle_next_button_click(self) -> None:
        pass

class DemoState(State):
    def __init__(self, demo_box, key):
        super().__init__()
        self.__demo_box = demo_box
        self.__key = key
        self.__next_state = None

    @property
    def demo_box(self):
        return self.__demo_box

    @property
    def key(self):
        return self.__key

    @property
    def next_state(self):
        return self.__next_state

    @next_state.setter
    def next_state(self, state: State):
        self.__next_state = state

    @property
    def demo_box(self):
        return self.__demo_box

    def handle_next_button_click(self):
        if self.__next_state:
            self.__next_state.execute()
            self.context.value = self.__next_state.__class__.__name__
            self.context.transition_to(self.__next_state)

    def execute(self):
        pass


class Demonstrator(widgets.VBox):
    def __init__(self, demo_box: widgets.Box, state_list: Type[DemoState], **kwargs):
        self.__demo_box = demo_box()
        self.__state_list = state_list
        self.__state_name_list = [state.__name__ for state in self.__state_list]
        self.__state_instances = self.__construct_state_list_instances()
        self.__context = Context(self.__state_instances[0])
        self.__context.value = self.__state_name_list[0]
        self.__context.set_on_click_reset_button_additional_callback(
            self.__on_click_reset_button
        )
        self.__state_dropdown = widgets.Dropdown(
            options=self.__state_name_list,
            value=self.__state_name_list[0],
            description="state",
        )
        self.__state_dropdown.observe(self.__on_change_dropdown, "value")

        self.__state_hbox = widgets.HBox(
            [self.__context.hbox_buttons, self.__state_dropdown],
            layout={"border": "2px solid lightblue"},
        )
        self.__context.observe(self.__on_change_context, "value")

        super().__init__([self.__demo_box, self.__state_hbox], **kwargs)

    def __on_click_reset_button(self):
        self.__state_dropdown.value = self.__state_name_list[0]

    def __construct_state_list_instances(self):
        state_instance_list = list()
        state_number = len(self.__state_list)

        for i in list(range(state_number)):
            state_instance = self.__state_list[i](demo_box=self.__demo_box, key=i)
            state_instance_list.append(state_instance)

        for i in list(range(0, state_number - 1)):
            state_instance_list[i].next_state = state_instance_list[i + 1]

        state_instance_list[-1].next_state = state_instance_list[0]
        return state_instance_list

    def __on_change_context(self, change):
        self.__state_dropdown.value = change["new"]

    def __on_change_dropdown(self, change):
        new_value = change["new"]
        self.__context.value = new_value
        index = self.__state_name_list.index(new_value)
        self.__state_instances[index].execute()
        self.__context.transition_to(self.__state_instances[index])
