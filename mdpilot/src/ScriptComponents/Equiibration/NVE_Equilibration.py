import EquilibrationComponent


class NVE_EquilibrationComponent(EquilibrationComponent):

    def __init__(self):
        super().__init__()
        # init other properties here
        '''
        N: number of particles
        V: volume
        E: total energy
        KE: kinetic energy
        PE: potential energy
        '''
        self.N = 0 
        self.V = 0
        self.E = 0

    def get_equilibration_property(self):
        pass

    def generate_script_text(self):
        pass