import ipywidgets as widgets
import threading
import components.ForegroundPages as pages
from components.UserDB import user_db
from IPython.core.display import display


class _SRV360Button(widgets.Button):
    def __init__(self, icon: str, button_style="danger", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.button_style = button_style
        self.layout = widgets.Layout(width="auto")


class SRV360SettingPage(widgets.VBox):
    CLOSESPEED_KEY = 'SRV360AppCloseSpeed'
    CLOSESPEED_15KM = "15km/h"
    CLOSESPEED_25KM = "25km/h"
    CLOSESPEED_35KM = "35km/h"

    def __init__(self, title="SRV360 Setting", **kwargs):

        self.__title = widgets.HTML(
            f"<h4 style='font-weight:bold; color:white'>{title}</h4>")
        
        __user_setting_closespeed = user_db.get_user_setting(self.CLOSESPEED_KEY)
        self.__closespeed_setting_buttons = widgets.ToggleButtons(
            options=[self.CLOSESPEED_15KM,
                     self.CLOSESPEED_25KM, self.CLOSESPEED_35KM],
            # description="CloseSpeed",
            value=__user_setting_closespeed if __user_setting_closespeed else self.CLOSESPEED_15KM,
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
        
        
        self.__external_closespeed_setting_callback_list = []
        
        super().__init__(children=[self.__title,
                                   self.__closespeed_setting,
                                   self.__exit_button], **kwargs)
        
        self.__closespeed_setting_buttons.observe(self.__on_change_closespeed_setting, "value")
        
    @property
    def exit_setting_button(self):
        return self.__exit_button
    
    def __on_change_closespeed_setting(self, change):
        new_value = change["new"]
        user_db.save_userdb(key=self.CLOSESPEED_KEY, value=new_value)
        
        for callback in self.__external_closespeed_setting_callback_list:
            callback(new_value)
            
    def append_closespeed_setting_callback(self, callback):
        self.__external_closespeed_setting_callback_list.append(callback)
                        
        
    @property
    def user_setting_closespeed_value(self):
        return self.__closespeed_setting_buttons.value    
    


class SRV360Page(widgets.VBox):

    def __init__(self, **kwargs):
        self.__main_output = widgets.Output()
        self.__main_page = pages.SRV360_PAGE_0
        self.__home_button = _SRV360Button(icon="home")
        self.__setting_button = _SRV360Button(icon="gear")
        self.__buttons_box = widgets.HBox(
            [self.__home_button, self.__setting_button])

        with self.__main_output:
            display(self.__main_page)

        self.__srv360_setting_page = SRV360SettingPage()
        self.__setting_event = threading.Event()

        super().__init__(
            children=[self.__buttons_box, self.__main_output], **kwargs)

        self.__setting_button.on_click(self.__on_click_setting_button)
        self.__srv360_setting_page.exit_setting_button.on_click(self.__on_click_exit_setting_button)
        

    @property
    def srv360_setting_page(self):
        return self.__srv360_setting_page
    
    @property
    def home_button(self):
        return self.__home_button

    @property
    def setting_button(self):
        return self.__setting_button
    
    def clear_setting(self):
        self.__setting_event.clear()
        
    def exit_setting_page(self):
        self.__main_output.clear_output()
        self.__setting_event.clear()
        with self.__main_output:
            display(self.__main_page)
        
    def __on_click_exit_setting_button(self, button):
        self.exit_setting_page()

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
                display(self.__srv360_setting_page)    
                
                