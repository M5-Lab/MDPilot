import EquilibrationComponent

class NPT_EquilibrationComponent(EquilibrationComponent):

    def __init__(self):
        super().__init__()
        #init other properties here
        self.T = 0
        self.P = 0
        self.N = 0

    def get_equilibration_property(self):
        pass

    def generate_script_text(self):
        pass