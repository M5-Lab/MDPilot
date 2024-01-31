import numpy as np
import AbstractScriptComponent as AbstractScriptComponent
import NVE_Equilibration, NPT_Equilibration, NVT_Equilibration

class EquilibrationComponent(AbstractScriptComponent):
    # This class cannot be constructed because it does not implement 
    # the abstract method generate_script_text. However, the child classes
    # which inhert EquilibrationComponent will implement this method and can use
    # the methods implemented in this class.
    
    def __init__(self):
        pass

    def is_equilibrated(self, properties : list[list], tol : float):
        """
        Args:
            property: list of properties to check equilibration
            tol: tolerance for equilibration

        i.e. For the NVT ensemble, we check if temperature is equilibrated via the relation 
            |var(T) - (kB*T_target^2)^2/var(E)| < tol 
            var(T) is the variance of the temperature
            var(E) is the variance of the total energy
            kB is Boltzmann's constant
            T_target is the target temperature
        """
        pass


        
        

    def get_equilibration_property(self):
        pass


def construct_equilibration_component(property : str):
    """
    Factory Method: Create a EquilibrationComponent for the specified property.

    Args:
        property (str): The language for which to create a localizer.

    Returns:
        EquilibrationComponent: An instance of the EquilibrationComponent for the specified property.
    """
    equilibration_components = {
        "NPT": NPT_Equilibration,
        "NVT": NVT_Equilibration,
        "NVE": NVE_Equilibration,
    }

    if property not in equilibration_components.keys():
        raise KeyError(f"Invalid equilibration property: {property}. Must be NPT, NVE or NVT")

    return equilibration_components[property]()