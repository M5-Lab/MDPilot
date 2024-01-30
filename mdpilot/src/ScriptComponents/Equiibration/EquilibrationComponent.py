from abc import ABC, abstractmethod

import ScriptComponent
import EnergyEquilibrationComponent, DensityEquilibrationComponent, \
         PressureEquilibrationComponent, TempeartureEquilibrationComponent

class EquilibrationComponent(ABC, ScriptComponent):

    def __init__(self):
        super().__init__(self)
        #init other properties here

    @abstractmethod
    def get_equilibration_property(self):
        pass

    def is_equilibrated(self):
        #use self.get_equilibration_property() to implment generic version
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
        "Pressure": PressureEquilibrationComponent,
        "Temperature": TempeartureEquilibrationComponent,
        "Density": DensityEquilibrationComponent,
        "Energy" : EnergyEquilibrationComponent
    }

    if property not in equilibration_components.keys():
        raise KeyError(f"Invalid equilibration property: {property}. Must be 'Pressure', 'Temperature', 'Density', or 'Energy'")

    return equilibration_components[property]()