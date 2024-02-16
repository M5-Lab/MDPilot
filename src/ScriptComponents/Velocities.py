from .AbstractScriptComponent import AbstractScriptComponent
import numpy as np

class Velocities(AbstractScriptComponent):

    """
    T is the temeparture to initialize the velocities to match. This can be passed as a number,
    or as the name of a variable that will be set in the LAMMPS script. If the latter,
    set the flag `is_var` to True.
    """
    def __init__(self, T, is_var = False):
        self.T = T
        self.is_var = is_var

        if is_var and (" " in T):
            raise ValueError("Variable names cannot contain spaces.")


    def generate_script_text(self):
        vel_seed = f"{np.random.randint(1000,1000000)}"
        if self.is_var:
            return f"velocity all create ${{{self.T}}} {vel_seed} dist gaussian mom yes"
        else:
            return f"velocity all create {self.T} {vel_seed} dist gaussian mom yes"

