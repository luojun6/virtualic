import ipywidgets as widgets


class DockButton(widgets.Button):
    def __init__(self, icon: str, button_style="info", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.button_style = button_style
        self.layout = widgets.Layout(width="auto")


class DockButtons(widgets.VBox):

    def __init__(self, **kwargs):

        self.__home_button = DockButton(icon="home")
        self.__music_button = DockButton(icon="music")
        self.__radio_button = DockButton(icon="")
        self.__radio_button.description = "𝗥"
        self.__setting_button = DockButton(icon="gear")
        self.__car_button = DockButton(icon="car")
        self.__avm360_button = DockButton(icon="camera")
        self.__bars_button = DockButton(icon="bars")

        self.layout = widgets.Layout(padding="3px")

        super().__init__(
            children=[
                self.__home_button,
                self.__music_button,
                self.__radio_button,
                self.__setting_button,
                self.__car_button,
                self.__avm360_button,
                self.__bars_button
            ],
            **kwargs)

    @property
    def home_button(self):
        return self.__home_button

    @property
    def music_button(self):
        return self.__music_button

    @property
    def setting_button(self):
        return self.__setting_button

    @property
    def car_button(self):
        return self.__car_button

    @property
    def avm360_button(self):
        return self.__avm360_button

    @property
    def bars_button(self):
        return self.__bars_button

    @property
    def dock_buttons(self):
        return self.__dock_buttons

dock_buttons = DockButtons()