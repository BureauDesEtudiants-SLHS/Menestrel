import json
import locale
import datetime
import os

class Theme:

    def __init__(self, month, theme, color, fonts, font_color, background, origine="", voeux=""):
        self.month = month
        self.theme = theme
        self.color = color
        self.fonts = fonts
        self.font_color = font_color
        self.background = background
        self.origine = origine
        self.voeux = voeux

    @staticmethod
    def hexa2RGB(color):
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        return r, g, b

    def getRGBcolor(self):
        return self.hexa2RGB(self.color)

    def getRGBfont(self):
        return self.hexa2RGB(self.font_color)

    @staticmethod
    def load_themes(file_path=None):

        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/themes.json"

        with open(file_path, "r") as f:
            themes_data = json.load(f)

        themes = []
        for theme_data in themes_data["themes"]:
            theme = Theme(**theme_data)
            themes.append(theme)

        return themes

    @staticmethod
    def save_themes(themes, file_path=None):
        
        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/themes.json"

        themes_data = {"themes": [theme.__dict__ for theme in themes]}

        with open(file_path, "w") as f:
            json.dump(themes_data, f, indent=4)

    def __str__(self):
        return json.dumps(vars(self), indent=4)

    def get_fonts_path(self):
        repertoire = os.getcwd()
        paths = {
            "title": f"{repertoire}/assets/fonts/{self.fonts["title"]}",
            "text": f"{repertoire}/assets/fonts/{self.fonts["text"]}"
        }

        return paths

    @staticmethod
    def get_theme_from_month(month, themes):

        for theme in themes:
            if theme.month == month:
                return theme
        return None
