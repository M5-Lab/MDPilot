from .AbstractScriptComponent import AbstractScriptComponent
import os

class Geometry(AbstractScriptComponent):

    def __init__(self, geom_file_path : str = None):
        self.geom_file_path = geom_file_path


    def generate_script_text(self):
        if os.path.exists(self.geom_file_path):
            return f"read_data {self.geom_file_path}\n"
        else:
            raise FileNotFoundError(f"Geometry file not found: {self.geom_file_path}")