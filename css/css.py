import os
import pathlib

# from IPython.display import HTML
from urllib.request import urlopen


# Check how to set css via demo_components.ipynb
BACKGROUND_scree_off = "screen_off"
BACKGROUND_theme_night = "theme_night"
FONT_color_night = "font_color_night"
FONT_color_day = "font_color_day"

def get_css_html(css_name = "theme"):

    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    theme_css_path = os.path.join(parent_dir, f"css/{css_name}.html")
    theme_css_url = pathlib.Path(theme_css_path).as_uri()
    html = urlopen(theme_css_url)

    # HTML(html.read().decode('utf-8'))

    return html
