import ipywidgets as widgets
import threading
import components.ForgroundPages as pages
from IPython.core.display import display


class AVM360Button(widgets.Button):
    def __init__(self, icon: str, button_style="danger", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.button_style = button_style
        self.layout = widgets.Layout(width="auto")


class AVM360SettingPage(widgets.VBox):
    CLOSESPEED_15KM = "15km"
    CLOSESPEED_25KM = "25km"
    CLOSESPEED_35KM = "35km"

    def __init__(self, title="AVM360 Setting", **kwargs):

        self.__title = widgets.HTML(
            f"<h4 style='font-weight:bold; color:white'>{title}</h4>")
        self.__closespeed_setting_buttons = widgets.ToggleButtons(
            options=[self.CLOSESPEED_15KM,
                     self.CLOSESPEED_25KM, self.CLOSESPEED_35KM],
            # description="CloseSpeed",
            button_style="info",
            # style={"button_width": "auto"}
            # layout=widgets.Layout(width='auto')
        )
        self.__closespeed_setting = widgets.VBox([
            widgets.HTML(
                f"<p style='font-weight:bold; color:white'>Close Speed Setting</p>"),
            self.__closespeed_setting_buttons
        ])
        self.__exit_button = widgets.Button(
            icon="xmark", description="Exit Setting", button_style="danger")
        super().__init__(children=[self.__title,
                                   self.__closespeed_setting,
                                   self.__exit_button], **kwargs)
    @property
    def exit_setting_button(self):
        return self.__exit_button
    


class AVM360Page(widgets.VBox):

    def __init__(self, **kwargs):
        self.__main_output = widgets.Output()
        self.__main_page = pages.AVM360_PAGE_0
        self.__home_button = AVM360Button(icon="home")
        self.__setting_button = AVM360Button(icon="gear")
        self.__buttons_box = widgets.HBox(
            [self.__home_button, self.__setting_button])

        with self.__main_output:
            display(self.__main_page)

        self.__avm360_setting_page = AVM360SettingPage()
        self.__setting_event = threading.Event()

        super().__init__(
            children=[self.__buttons_box, self.__main_output], **kwargs)

        self.__setting_button.on_click(self.__on_click_setting_button)
        self.__avm360_setting_page.exit_setting_button.on_click(self.__on_click_exit_setting_button)

    @property
    def home_button(self):
        return self.__home_button

    @property
    def setting_button(self):
        return self.__setting_button
    
    def __on_click_exit_setting_button(self, button):
        self.__main_output.clear_output()
        with self.__main_output:
            display(self.__main_page)

    def __on_click_setting_button(self, button):
        if self.__setting_event.is_set():
            self.__setting_event.clear()
            self.__main_output.clear_output()
            with self.__main_output:
                display(self.__main_page)

        else:
            self.__setting_event.set()
            self.__main_output.clear_output()
            with self.__main_output:
                display(self.__avm360_setting_page)
