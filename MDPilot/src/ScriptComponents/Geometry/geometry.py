import AbstractScriptComponent


class Geometry(AbstractScriptComponent):

    def __init__(self, geom_file_path : str = None):
        self.geom_file_path = geom_file_path


    def generate_script_text(self):
        read_data = f"read_data {self.geom_file_path}\n"