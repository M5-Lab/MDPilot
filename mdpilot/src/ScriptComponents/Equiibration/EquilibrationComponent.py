import numpy as np
import AbstractScriptComponent as AbstractScriptComponent
import NVE_Equilibration, NPT_Equilibration, NVT_Equilibration

class EquilibrationComponent(AbstractScriptComponent):
    # This class cannot be constructed because it does not implement 
    # the abstract method generate_script_text. However, the child classes
    # which inhert EquilibrationComponent will implement this method and can use
    # the methods implemented in this class.
    
    def __init__(self, properties : list[list]):
        # property: list of list of properties sampled over time 
        pass


    def is_equilibrated(self, property_idx: int, target: float, tol : float):
        """
        Args:
            tol: tolerance for equilibration
        """
        property = self.properties[property_idx]
        samples = len(property)
        prop_cum = np.abs(np.cumsum(property) / (np.arange(samples) + 1) - target)
        return np.all(prop_cum[int(0.9*samples):] < tol) # at least last 10% of the time series are near target value within tolerance



        


        
        

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