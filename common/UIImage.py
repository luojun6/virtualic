import ipywidgets as widgets
from IPython.core.display import display


def create_image_object(image_path: str):
    """A simple function to create ipywidgets.Image object

    Args:
        image_path (str): The absolute path of image_path.

    Returns:
        _type_: An ipywidgets.Image object
    """

    image_type = image_path.split(".")[-1]

    image = open(image_path, "rb").read()
    return widgets.Image(value=image, format=image_type)


class ImageDisplayer(widgets.VBox):
    NO_DISPLAY = "NO_DISPLAY"

    def __init__(self, img_dict: dict, title="ImageDisplayer", **kwargs):

        self.__title = widgets.HTML(value=f"<h2>{title}</h2>")
        self.__img_dict = img_dict
        self.__construct_img_obj()
        self.__img_dict[self.NO_DISPLAY] = self.NO_DISPLAY
        self.__dropdown = widgets.Dropdown(
            options=list(img_dict.keys()), value=self.__img_dict[self.NO_DISPLAY]
        )
        self.__out = widgets.Output()

        self.__dropdown.observe(self.__on_change_dropdown, "value")

        super().__init__([self.__title, self.__dropdown, self.__out], **kwargs)

    def __construct_img_obj(self):
        for img in list(self.__img_dict.keys()):
            self.__img_dict[img] = create_image_object(self.__img_dict[img])

    def __on_change_dropdown(self, change):
        new_value = change["new"]
        self.__out.clear_output()

        if new_value == self.NO_DISPLAY:
            return

        with self.__out:
            display(self.__img_dict[new_value])
