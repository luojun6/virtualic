import ipywidgets as widgets

class SdCardPluginStatus(widgets.RadioButtons):
    SD_CARD_PLUG_IN = "SD_CARD_PLUG_IN"
    SD_CARD_NOT_PLUG_IN = "SD_CARD_NOT_PLUG_IN"
    
    def __init__(self):
        
        # self.options = [self.SD_CARD_NOT_PLUG_IN, self.SD_CARD_PLUG_IN]
        # self.value=self.SD_CARD_NOT_PLUG_IN
        # self.description="SD Card Plug-in Status"
        super().__init__(
            options = [self.SD_CARD_NOT_PLUG_IN, self.SD_CARD_PLUG_IN],
            value = self.SD_CARD_NOT_PLUG_IN,
            description="SDCardSts"
        )