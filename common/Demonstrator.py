from typing import Type
import ipywidgets as widgets


from common.AbstractState import Context, State


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
