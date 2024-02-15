from .AbstractScriptComponent import AbstractScriptComponent


class Potential(AbstractScriptComponent):

    def __init__(self, pot_file_path : str = None):
        self.pot_file_path = pot_file_path


    def generate_script_text(self):
        pass
        #& @NICK idk how you load a potential from a file but do that here

