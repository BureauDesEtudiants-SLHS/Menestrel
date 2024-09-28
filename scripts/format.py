import json
import os

class Format:

    def __init__(self, name, size, logo_size, positions, font_sizes):
        self.name = name
        self.size = size
        self.logo_size = logo_size
        self.positions = positions
        self.font_sizes = font_sizes

    @staticmethod
    def load_formats(file_path=None):
        
        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/formats.json"

        with open(file_path, 'r') as file:
            formats_data = json.load(file)
        
        return [Format(**format) for format in formats_data]

    def save_format(self, file_path=None):

        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/formats.json"

        try:
            with open(file_path, 'r') as file:
                formats_data = json.load(file)
        except FileNotFoundError:
            formats_data = []

        formats_data.append(self.__dict__)

        with open(file_path, 'w') as file:
            json.dump(formats_data, file, indent=4)
    
    def __str__(self):
        return json.dumps(vars(self), indent=4)
