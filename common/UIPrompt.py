import ipywidgets as widgets
from time import sleep
from utils.threading_timer import debounce

class UIPromptText(widgets.Text):
    duration = 5

    def __init__(self, debug=False, *args, **kwargs):
        self.value = ""
        self.__debug = debug
        super().__init__(*args, **kwargs)

    def prompt(self, msg: str):
        self.value = msg
        self.reset()
        if self.__debug:
            print(f"Start UIPrompt {self.duration}s timer.")
            for i in range(self.duration):
                sleep(1)
                print(f"{i + 1}s")

    @debounce(duration)
    def reset(self):
        self.__init__()


class UIPromptText3s(UIPromptText):
    duration = 3
    @debounce(duration)
    def reset(self):
        return super().reset()


class UIPromptText5s(UIPromptText):
    pass


class UIPromptText10s(UIPromptText):
    duration = 10
    @debounce(duration)
    def reset(self):
        return super().reset()